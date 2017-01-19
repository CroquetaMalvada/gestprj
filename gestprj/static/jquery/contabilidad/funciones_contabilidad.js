$(window).on('beforeunload', function() {
  loading("Carregant...",true);
});
$(document).ready(function(){
    $(document).find("#loading").dialog("close");
    $("#data_min").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date(1997, 0, 1)});//minDate: (new Date(1997, 1 - 1 , 1)), maxDate: 0
    $("#data_max").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date() });
    //asignarles un valor por defecto
    $("#data_min").datepicker("setDate", new Date(1997, 0, 1));
    $("#data_max").datepicker("setDate", new Date());



//EFECTOS ACCORDION
    $("#accordion").accordion({
        collapsible: true,
        heightStyle: "content",
        create: function(){
            $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
        },
        activate: function(){
            $.fn.dataTable.tables( {visible: false, api: true} ).columns.adjust();///IMPORTANTE sirve para alinear correctamente las cabezeras de las datatables,ya que con divs que estan hidden no se alineaban automaticamente
        }
    });

    $("input[name=opcio_cont]").on("click",function(){
        if($(this).val()==1)
            $("#formulario_projectes_cont").attr("action","/cont_dades/");
        else if($(this).val()==2)
            $("#formulario_projectes_cont").attr("action","/cont_estat_pres/");
        else if($(this).val()==3)
            $("#formulario_projectes_cont").attr("action","/cont_despeses/");
        else if($(this).val()==4)
            $("#formulario_projectes_cont").attr("action","/cont_ingresos/");
        else if($(this).val()==5)
            $("#formulario_projectes_cont").attr("action","/cont_estat_prj_resp/");
        else if($(this).val()==6)
            $("#formulario_projectes_cont").attr("action","/cont_fitxa_major_prj/");
        else if($(this).val()==7)
            $("#formulario_projectes_cont").attr("action","/cont_resum_fitxa_major_prj/");
        else if($(this).val()==8)
            $("#formulario_projectes_cont").attr("action","/cont_resum_estat_prj/");
        else if($(this).val()==9)
            $("#formulario_projectes_cont").attr("action","/cont_resum_estat_canon_prj_resp/"); ////TERMINAR
        else if($(this).val()==10)
            $("#formulario_projectes_cont").attr("action","/cont_comptes_no_asignats/"); ////TERMINAR
    });
});