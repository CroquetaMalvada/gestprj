from __builtin__ import int
from django.db import connections
from gestprj.models import Projectes,Responsables,Financadors, CentresParticipants, PersonalCreaf, PersonalExtern, Financadors, Receptors, Renovacions, Pressupost, PeriodicitatPartida
from decimal import *


def dictfetchall(cursor):
    # Devuelve todos los campos de cada row como una lista
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def ContDades(projectes):

        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj

            centres_participants = CentresParticipants.objects.filter(id_projecte= projecte.id_projecte)
            participants_creaf = PersonalCreaf.objects.filter(id_projecte=projecte.id_projecte)
            participants_externs = PersonalExtern.objects.filter(id_projecte=projecte.id_projecte)

            financadors = Financadors.objects.filter(id_projecte=projecte.id_projecte)
            receptors = Receptors.objects.filter(id_projecte=projecte.id_projecte)

        # CANON I IVA
            concedit=0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = round(concedit + float(importe.import_concedit),2)
            #vienen en la tabla:
            percen_iva = round(projecte.percen_iva,2)
            percen_canon_creaf = round(projecte.percen_canon_creaf,2)
            canon_oficial = round(projecte.canon_oficial,2)

            # calculados a mano
            if concedit == 0: # para evitar problemas con la division si es 0
                percen_canon_oficial = 0.00
            else:
                percen_canon_oficial = round(((canon_oficial / concedit)*(100*(1+percen_iva/100))),2)
            canon_creaf = round(((concedit*percen_canon_creaf)/(100*(1+percen_iva/100))),2)
            diferencia_per = round((percen_canon_oficial-percen_canon_creaf),2)
            diferencia_eur = round((canon_oficial - canon_creaf),2)
            iva = round((( concedit * percen_iva ) / (100*(1+percen_iva/100))),2)

            canoniva = {"percen_iva":percen_iva,"percen_canon_creaf":percen_canon_creaf,"canon_oficial":canon_oficial,"percen_canon_oficial":percen_canon_oficial,"canon_creaf":canon_creaf,"diferencia_per":diferencia_per,"diferencia_eur":diferencia_eur,"iva":iva}
        ####

        # DESPESES
            despeses = []
            despesa_total_concedit = 0
            despesa_total_iva = 0
            despesa_total_canon = 0
            despesa_total_net = 0
            for despesa in Renovacions.objects.filter(id_projecte=projecte.id_projecte):
                import_concedit = float(despesa.import_concedit)
                despesa_total_concedit = despesa_total_concedit+import_concedit
                iva = round((( import_concedit * percen_iva ) / 100),2)
                despesa_total_iva = despesa_total_iva+iva
                canon = round((( import_concedit * percen_canon_creaf ) / 100),2)
                despesa_total_canon = despesa_total_canon+canon
                net = round(( import_concedit - iva - canon ),2)
                despesa_total_net = despesa_total_net+net
                despeses.append({"data_inici":despesa.data_inici,"data_fi":despesa.data_fi,"concedit":import_concedit,"iva":iva,"canon":canon,"net":net})
                # concedit = round(concedit + float(importe.import_concedit),2)

        ####

        # PRESSUPOST
            partides = []
            max_periodes = 0;
            # al suma de cada periodo
            totals = [0,0,0,0,0,0,0,0]
            total_import = 0
            partida_total = 0

            # primero vemos cual es el max de periodos que tiene una de als partidas
            for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):
                n_periodes = 0
                for periode in PeriodicitatPartida.objects.filter(id_partida=partida.id_partida):
                    n_periodes = n_periodes+1
                    if n_periodes > max_periodes:
                        max_periodes = n_periodes
            ######

            # Despues ponesmos los periodos en cada partida,usamos el max anterior para rellenar con 0 en caso de que haya menos periodos que el maximo
            for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):
                periodes = []
                total_periode = 0

                for index,periode in enumerate(PeriodicitatPartida.objects.filter(id_partida=partida.id_partida)):
                    total_periode = total_periode+periode.import_field
                    totals[index] = totals[index]+periode.import_field
                    periodes.append({"importe":periode.import_field})

                if len(periodes) < max_periodes:
                    for dif in range((max_periodes-len(periodes))):
                        periodes.append({"importe":0.00})

                totals[max_periodes] = totals[max_periodes]+total_periode

            ######

                # Si no hay periodos,comprovar si las propias partidas tienen importe:
                if not periodes:
                    total_import = total_import+partida.import_field
                    partides.append({"concepte":partida.id_concepte_pres.desc_concepte,"import":partida.import_field})
                else:
                    partides.append({"concepte":partida.id_concepte_pres.desc_concepte,"periodes":periodes,"total":total_periode})

                ######
        ########


            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)

            #####
            # tam_periodes = round(max_periodes/8) #lo dividimos entre 8 para el boostrap,ya que quedan col-md-8 como tamano maximo(hay 2 divs que ocupan 2,el concepto y el total)
            resultado.append({"dades_prj":projecte,"codi_resp":cod_responsable,"codi_prj":cod_projecte,'centres_participants':centres_participants,'participants_creaf':participants_creaf,'participants_externs':participants_externs,'financadors':financadors,'receptors':receptors,'canoniva':canoniva,'despeses':despeses,'total_concedit':despesa_total_concedit,'total_iva':despesa_total_iva,'total_canon':despesa_total_canon,'total_net':despesa_total_net,'partides':partides,'totals_pres':totals,'max_periodes':range(max_periodes),'total_import_pres':total_import})

        return resultado

def ContEstatPres(projectes):


        ##### NO ESTA ACABADO TODAVIA


        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):
            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            codigo_entero=cod_responsable+cod_projecte
            #####
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = concedit + importe.import_concedit
            iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
            canon = ( concedit * projecte.percen_canon_creaf ) / ( 100 * (1+projecte.percen_iva/100) )
            net_disponible = concedit-iva-canon

            round(concedit,2)
            round(iva,2)
            round(canon,2)
            round(net_disponible,2)
            #####

        # PRESSUPOST
            partides = []
            max_periodes = 0;
            # al suma de cada periodo
            totals = [0,0,0,0,0,0,0,0]
            total_import = 0
            partida_total = 0

            # primero vemos cual es el max de periodos que tiene una de als partidas
            for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):
                n_periodes = 0
                for periode in PeriodicitatPartida.objects.filter(id_partida=partida.id_partida):
                    n_periodes = n_periodes+1
                    if n_periodes > max_periodes:
                        max_periodes = n_periodes
            ######

            # Despues ponesmos los periodos en cada partida,usamos el max anterior para rellenar con 0 en caso de que haya menos periodos que el maximo
            periodes = []

            for n in range(0,max_periodes):
                for partida in Pressupost.objects.filter(id_projecte=projecte.id_projecte):
                    for index,periode in enumerate(PeriodicitatPartida.objects.filter(id_partida=partida.id_partida)):
                        if index == n:
                            periodes.n.append({"num":n,"import":partida.import_field})

                        # total_periode = total_periode+periode.import_field
                        # totals[index] = totals[index]+periode.import_field
                        # periodes.append({"importe":periode.import_field})

                if len(periodes) < max_periodes:
                    for dif in range((max_periodes-len(periodes))):
                        periodes.append({"importe":0.00})

                # totals[max_periodes] = totals[max_periodes]+total_periode

            ######

                # Si no hay periodos,comprovar si las propias partidas tienen importe:
                # if not periodes:
                #     total_import = total_import+partida.import_field
                #     partides.append({"concepte":partida.id_concepte_pres.desc_concepte,"import":partida.import_field})
                # else:
                #     partides.append({"concepte":partida.id_concepte_pres.desc_concepte,"periodes":periodes,"total":total_periode})

                ######
        ########


            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)

            #####
            # tam_periodes = round(max_periodes/8) #lo dividimos entre 8 para el boostrap,ya que quedan col-md-8 como tamano maximo(hay 2 divs que ocupan 2,el concepto y el total)
            resultado.append({"dades_prj":projecte,"codi_resp":cod_responsable,"codi_prj":cod_projecte,'centres_participants':centres_participants,'participants_creaf':participants_creaf,'participants_externs':participants_externs,'financadors':financadors,'receptors':receptors,'canoniva':canoniva,'despeses':despeses,'total_concedit':despesa_total_concedit,'total_iva':despesa_total_iva,'total_canon':despesa_total_canon,'total_net':despesa_total_net,'partides':partides,'totals_pres':totals,'max_periodes':range(max_periodes),'total_import_pres':total_import,'periodes':periodes})

        return resultado

def ContDespeses(projectes):
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            codigo_entero=cod_responsable+cod_projecte
            #####
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = concedit + importe.import_concedit
            iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
            canon = ( concedit * projecte.percen_canon_creaf ) / ( 100 * (1+projecte.percen_iva/100) )
            net_disponible = concedit-iva-canon

            concedit = round(concedit,2)
            iva = round(iva,2)
            canon = round(canon,2)
            net_disponible = round(net_disponible,2)
            #####

            # 105 en el convert equivale al dd-mm-yyyy
            cursor.execute("SELECT TOP 100 PERCENT CONVERT(VARCHAR,Fecha,105)as Data, Asiento, Documento, Cuenta, Opc1, Opc3, Descripcion, Opc2, Debe, Haber FROM  Apuntes WHERE ((Diario='0' OR Diario='1' OR Diario='4') AND (((Cuenta LIKE '2%'+(?)) OR (Cuenta LIKE '6%'+(?))) AND (Cuenta <> '6296'+(?))) AND ((Fecha >= CONVERT(date,(?),105)) AND (Fecha<=CONVERT(date,(?),105)))) ORDER BY Fecha",[codigo_entero,codigo_entero,codigo_entero,fecha_min,fecha_max])
            projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve

            ##### Para ir restando el saldo a medida que salen gastos:
            saldo_disponible = float(net_disponible)
            total_despeses = 0
            for prjfet in projectfetch:
                if prjfet["Debe"] == None:
                    prjfet["Debe"] = 0
                else:
                    saldo_disponible = saldo_disponible - prjfet["Debe"]
                    total_despeses = total_despeses+prjfet["Debe"]

                if saldo_disponible<0.1 and saldo_disponible>-0.1: # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
                    saldo_disponible = 0

                prjfet["saldo_disponible"] = saldo_disponible

            #####
            total_disponible = saldo_disponible

            ##### poner 0 en los codigos si son demasiado cortos para tener x tamano

            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)
            #####
            resultado.append({"dades_prj":projecte,"despeses":projectfetch,"concedit":concedit,"iva_percen":float(projecte.percen_iva),"iva":iva,"canon_percen":float(projecte.percen_canon_creaf),"canon":canon,"net_disponible":net_disponible,"total_despeses":total_despeses,"total_disponible":total_disponible,'data_min':fecha_min,'data_max':fecha_max,"codi_resp":cod_responsable,"codi_prj":cod_projecte})

        return resultado


def ContIngresos(projectes):
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            codigo_entero=cod_responsable+cod_projecte
            #####
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = concedit + importe.import_concedit
            iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
            net_disponible = concedit-iva
            #####

            # 105 en el convert equivale al dd-mm-yyyy
            cursor.execute("SELECT TOP 100 PERCENT CONVERT(VARCHAR,Fecha,105)as Data, Asiento, Cuenta, Descripcion, Debe, Haber FROM  Apuntes WHERE ((Diario='0' OR Diario='1' OR Diario='4') AND (Cuenta LIKE '7%'+(?)) AND (Cuenta <> '6296'+(?)) AND ((Fecha >= CONVERT(date,(?),105)) AND (Fecha<=CONVERT(date,(?),105)))) ORDER BY Fecha",[codigo_entero,codigo_entero,fecha_min,fecha_max])
            projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve

            ##### Para ir restando el saldo pendiente a medida que salen ingresos:
            saldo_pendiente = float(net_disponible)
            total_ingresos = 0
            for prjfet in projectfetch:
                if prjfet["Haber"] == None:
                    prjfet["Haber"] = 0
                else:
                    saldo_pendiente = saldo_pendiente - prjfet["Haber"]
                    total_ingresos = total_ingresos+prjfet["Haber"]

                if saldo_pendiente<0.1 and saldo_pendiente>-0.1: # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
                    saldo_pendiente = 0
                prjfet["saldo_pendiente"] = saldo_pendiente

            #####
            total_pendiente = saldo_pendiente

            ##### poner 0 en los codigos si son demasiado cortos para tener x tamano

            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)
            #####
            resultado.append({"dades_prj":projecte,"ingresos":projectfetch,"concedit":concedit,"iva_percen":float(projecte.percen_iva),"iva":iva,"net_disponible":net_disponible,"total_pendiente":total_pendiente,"total_ingresos":total_ingresos,'data_min':fecha_min,'data_max':fecha_max,"codi_resp":cod_responsable,"codi_prj":cod_projecte})

        return resultado

def ResumEstatProjectes(projectes):
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        investigadores = {} #diccionario
        proyectos = []
        nuevo_inv = 0 #es un chivato para indicar cuando empezamos a sumar los proyectos de otro investigador
        num_investigadores = 0
        # for projecte_chk in projectes.getlist("prj_select"):
        for projecte_chk in projectes.getlist("prj_select"):
            cod_responsable = projecte_chk.split("-")[0]
            if int(cod_responsable) not in investigadores:
                investigadores[int(cod_responsable)]=int(cod_responsable)
                num_investigadores=num_investigadores+1

        for inv in investigadores:
            nuevo_inv = 1
            for projecte_chk in projectes.getlist("prj_select"):
                cod_responsable = projecte_chk.split("-")[0]
                if(inv==int(cod_responsable)):
                    ##### Para extraer el objeto proyecto y el codigo:
                    id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
                    cod_projecte = projecte_chk.split("-")[1]
                    projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
                    codigo_entero=cod_responsable+cod_projecte
                    #####


                    cursor.execute("SELECT ingressosD, ingressosH, despesesD, despesesH, canonD, canonH FROM ( SELECT Sum(Debe) AS ingressosD, Sum(Haber) AS ingressosH FROM Apuntes WHERE(Diario='0' OR Diario='4' OR Diario='1') AND (Cuenta LIKE '7%'+(?) AND Cuenta<>'7900'+(?)) AND (Fecha<= CONVERT(date, (?),105))) as ingressos, ( SELECT Sum(Debe) AS despesesD, Sum(Haber) AS despesesH FROM Apuntes WHERE (Diario='0' OR Diario='4' OR Diario='1') AND ((Cuenta LIKE'6%'+(?) OR Cuenta LIKE'2%'+(?)) AND Cuenta<>'6296'+(?)) AND (Fecha<= CONVERT(date, (?),105))) as despeses, ( SELECT Sum(Debe) AS canonD, Sum(Haber) AS canonH FROM Apuntes WHERE (Diario='0' OR Diario='4' OR Diario='1') AND (Cuenta='7900'+(?) OR Cuenta='6296'+(?)) AND (Fecha<= CONVERT(date, (?),105))) as canon",[codigo_entero,codigo_entero,fecha_max,codigo_entero,codigo_entero,codigo_entero,fecha_max,codigo_entero,codigo_entero,fecha_max])
                    projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve


                    if nuevo_inv == 1:
                        nuevo_inv = 0
                        #comprobar que no haya nones con el primer fetch
                        if projectfetch[0]["ingressosD"] is None:
                            projectfetch[0]["ingressosD"] = 0
                        if projectfetch[0]["ingressosH"] is None:
                            projectfetch[0]["ingressosH"] = 0
                        if projectfetch[0]["despesesD"] is None:
                            projectfetch[0]["despesesD"] = 0
                        if projectfetch[0]["despesesH"] is None:
                            projectfetch[0]["despesesH"] = 0
                        if projectfetch[0]["canonD"] is None:
                            projectfetch[0]["canonD"] = 0
                        if projectfetch[0]["canonH"] is None:
                            projectfetch[0]["canonH"] = 0

                        iva=0

                        proyectos.append(projectfetch)
                    else:
                        #pese a la comprovacion anterior,nos hara falta quitar los none por cada proyecto
                        ingressosD=projectfetch[0]["ingressosD"]
                        ingressosH=projectfetch[0]["ingressosH"]
                        despesesD=projectfetch[0]["despesesD"]
                        despesesH=projectfetch[0]["despesesH"]
                        canonD=projectfetch[0]["canonD"]
                        canonH=projectfetch[0]["canonH"]

                        # if(iva<Financadorsprojecte.percen_iva)iva = Projectes.objects.get

                        if ingressosD is None :
                            ingressosD=0
                        if ingressosH is None :
                            ingressosH=0
                        if despesesD is None :
                            despesesD=0
                        if despesesH is None :
                            despesesH=0
                        if canonD is None :
                            canonD=0
                        if canonH is None :
                            canonH=0

                        proyectos[0][0]["cod_responsable"]=cod_responsable
                        proyectos[0][0]["nom_responsable"]=Responsables.objects.get(codi_resp=cod_responsable).id_usuari.nom_usuari
                        proyectos[0][0]["concedit"]=cod_responsable
                        proyectos[0][0]["iva"]=round(proyectos[0][0]["iva"])+round(proyectos[0][0]["iva"])
                        proyectos[0][0]["ingressosD"]=round(proyectos[0][0]["ingressosD"])+round(ingressosD)
                        proyectos[0][0]["ingressosH"]=round(proyectos[0][0]["ingressosH"])+round(ingressosH)
                        proyectos[0][0]["despesesD"]=round(proyectos[0][0]["despesesD"])+round(despesesD)
                        proyectos[0][0]["despesesH"]=round(proyectos[0][0]["despesesH"])+round(despesesH)
                        proyectos[0][0]["canonD"]=round(proyectos[0][0]["canonD"])+round(canonD)
                        proyectos[0][0]["canonH"]=round(proyectos[0][0]["canonH"])+round(canonH)
                        #
                        #
            resultado.append(proyectos)
            proyectos= []
                    # proyectos.append(int(investigadores[investigadores.index(cod_responsable)]))

        return resultado

def ResumFitxaMajorProjectes(projectes):
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            codigo_entero=cod_responsable+cod_projecte
            #####
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = concedit + importe.import_concedit
            iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
            canon = ( concedit * projecte.percen_canon_creaf ) / ( 100 * (1+projecte.percen_iva/100) )
            net_disponible = concedit-iva-canon

            concedit = round(concedit,2)
            iva = round(iva,2)
            canon = round(canon,2)
            net_disponible = round(net_disponible,2)
            #####
            cursor.execute("SELECT TOP 100 PERCENT Apuntes.Cuenta, Plan_cuentas.Titulo, Sum(Apuntes.Debe) AS TotalDebe, Sum(Apuntes.Haber) AS TotalHaber FROM Plan_cuentas LEFT JOIN Apuntes ON (Plan_cuentas.Cuenta = Apuntes.Cuenta) WHERE ( (Plan_cuentas.Nivel=0) AND (((Apuntes.Cuenta) LIKE '2%'+(?))OR((Apuntes.Cuenta) LIKE '6%'+(?) )OR((Apuntes.Cuenta) LIKE '7%'+(?))) AND ((Apuntes.Diario)='0' OR (Apuntes.Diario)='4' OR (Apuntes.Diario)='1') AND ((Apuntes.Fecha)>=CONVERT(date, (?),105) AND (Apuntes.Fecha)<=CONVERT(date, (?),105))) GROUP BY Apuntes.Cuenta, Plan_cuentas.Titulo ORDER BY Apuntes.Cuenta",[codigo_entero,codigo_entero,codigo_entero,fecha_min,fecha_max])
            projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve


            ##### Para ir restando el saldo a medida que salen gastos:
            total_disponible = 0 # ES EL SALDO INICIAL ****SIEMPRE ES 0???????
            total_debe = 0
            total_haber = 0
            for prjfet in projectfetch:
                if prjfet["TotalDebe"] == None:
                    prjfet["TotalDebe"] = 0
                if prjfet["TotalHaber"] == None:
                    prjfet["TotalHaber"] = 0

                total_debe = total_debe+prjfet["TotalDebe"]
                total_haber = total_haber+prjfet["TotalHaber"]
                total_disponible = total_disponible - prjfet["TotalDebe"] + prjfet["TotalHaber"]


                if total_disponible<0.1 and total_disponible>-0.1: # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
                    total_disponible = 0

                if total_debe<0.1 and total_debe>-0.1:
                    total_debe = 0

                if total_haber<0.1 and total_haber>-0.1:
                    total_haber = 0

                prjfet["Total_disponible"] = total_disponible

            #####
            total_disponible = round(total_disponible,2)
            total_debe = round(total_debe,2)
            total_haber = round(total_haber,2)
            ##### poner 0 en los codigos si son demasiado cortos para tener x tamano

            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)
            #####
            resultado.append({"dades_prj":projecte,"despeses":projectfetch,"concedit":concedit,"iva_percen":round(float(projecte.percen_iva),2),"iva":iva,"canon_percen":round(float(projecte.percen_canon_creaf),2),"canon":canon,"net_disponible":net_disponible,"total_disponible":total_disponible,"total_debe":total_debe,"total_haber":total_haber,'data_min':fecha_min,'data_max':fecha_max,"codi_resp":cod_responsable,"codi_prj":cod_projecte})

        return resultado


def FitxaMajorProjectes(projectes):
        fecha_min = projectes["data_min"]
        fecha_max = projectes["data_max"]
        cursor = connections['contabilitat'].cursor()
        resultado = []
        for projecte_chk in projectes.getlist("prj_select"):

            ##### Para extraer el objeto proyecto y el codigo:
            cod_responsable = projecte_chk.split("-")[0]
            id_resp = Responsables.objects.get(codi_resp=cod_responsable).id_resp
            cod_projecte = projecte_chk.split("-")[1]
            projecte = Projectes.objects.get(codi_prj=cod_projecte,id_resp=id_resp) # OJO!puede haber codi_prj duplicados en la bdd pero solo sacaremos un proyecto ya que es id_resp+codi_rpj
            codigo_entero=cod_responsable+cod_projecte
            #####
            ##### Cuentas:
            concedit = 0
            for importe in Financadors.objects.filter(id_projecte=projecte.id_projecte):
                concedit = concedit + importe.import_concedit
            iva = concedit - ( concedit / (1+projecte.percen_iva/100) )
            canon = ( concedit * projecte.percen_canon_creaf ) / ( 100 * (1+projecte.percen_iva/100) )
            net_disponible = concedit-iva-canon

            concedit = round(concedit,2)
            iva = round(iva,2)
            canon = round(canon,2)
            net_disponible = round(net_disponible,2)
            #####
            cursor.execute("SELECT TOP 100 PERCENT CONVERT(VARCHAR,Fecha,105) as Fecha, Asiento, Cuenta, Descripcion, Debe, Haber FROM  Apuntes WHERE ((Diario='0' OR Diario='1' OR Diario='4') AND ((Cuenta LIKE '2%'+(?)) OR (Cuenta LIKE '6%'+(?)) OR (Cuenta LIKE '7%'+(?))) AND ((Fecha >=CONVERT(date, (?),105)) AND (Fecha<=CONVERT(date, (?),105)))) ORDER BY Fecha",[codigo_entero,codigo_entero,codigo_entero,fecha_min,fecha_max])
            projectfetch = dictfetchall(cursor) # un cursor.description tambien sirve


            ##### Para ir restando el saldo a medida que salen gastos:
            total_caja = 0 # ES EL SALDO INICIAL ****SIEMPRE ES 0???????
            total_debe = 0
            total_haber = 0
            for prjfet in projectfetch:
                if prjfet["Debe"] == None:
                    prjfet["Debe"] = 0
                if prjfet["Haber"] == None:
                    prjfet["Haber"] = 0

                total_debe = total_debe+prjfet["Debe"]
                total_haber = total_haber+prjfet["Haber"]
                total_caja = total_caja - prjfet["Debe"] + prjfet["Haber"]


                if total_caja<0.1 and total_caja>-0.1: # esto sirve para evitar el floating point arithmetic y que muestre 0 en lugar de un numero largisimo
                    total_disponible = 0

                if total_debe<0.1 and total_debe>-0.1:
                    total_debe = 0

                if total_haber<0.1 and total_haber>-0.1:
                    total_haber = 0

                prjfet["Total_caja"] = round(total_caja,2)

            #####
            total_caja = round(total_caja,2)
            total_debe = round(total_debe,2)
            total_haber = round(total_haber,2)
            ##### poner 0 en los codigos si son demasiado cortos para tener x tamano

            if int(cod_responsable) < 10:
                cod_responsable="0"+str(cod_responsable)
            if int(cod_projecte) < 100:
                if int(cod_projecte) < 10:
                    cod_projecte="00"+str(cod_projecte)
                else:
                    cod_projecte="0"+str(cod_projecte)
            #####
            resultado.append({"dades_prj":projecte,"despeses":projectfetch,"concedit":concedit,"iva_percen":round(float(projecte.percen_iva),2),"iva":iva,"canon_percen":round(float(projecte.percen_canon_creaf),2),"canon":canon,"net_disponible":net_disponible,"total_caja":total_caja,"total_debe":total_debe,"total_haber":total_haber,'data_min':fecha_min,'data_max':fecha_max,"codi_resp":cod_responsable,"codi_prj":cod_projecte})

        return resultado

