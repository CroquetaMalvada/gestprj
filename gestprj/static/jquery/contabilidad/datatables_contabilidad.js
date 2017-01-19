var table_projectes;
var table_responsables;

$(document).ready(function(){
    /////IDIOMA DATATABLES
    var opciones_idioma = {
        "decimal":        ",",
        "emptyTable":     "No s'han trobat dades",
        "info":           "", //Mostrant d'_START_ a _END_ de _TOTAL_ resultats
        "infoEmpty":      "0 resultats",
        "infoFiltered":   "(filtrats d'un total de _MAX_)",
        "infoPostFix":    "",
        "thousands":      ",",
        "lengthMenu":     "Show _MENU_ entries",
        "loadingRecords": "Carregant...",
        "processing":     "Processant...",
        "search":         "Buscar:",
        "zeroRecords":    "No s'han trobat resultats",
        "paginate": {
            "first":      "Primer",
            "last":       "Últim",
            "next":       "Següent",
            "previous":   "Anterior"
        },
        "aria": {
            "sortAscending":  ": activar per ordenar de forma ascendent",
            "sortDescending": ": activar per ordenar de forma descendent"
        }
    }


   if($("#table_llista_projectes_cont")){//PROYECTOS
        table_projectes= $("#table_llista_projectes_cont").DataTable({
            scrollY:        '70vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            order:          [[ 1, "asc" ]],
            columnDefs:[
                {"visible":false,"targets":[4]}
            ],
            language: opciones_idioma
        });
   }

   if($("#table_llista_responsables_cont")){//RESPONSABLES
       table_responsables = $("#table_llista_responsables_cont").DataTable({
            scrollY:        '70vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            order:          [[ 1, "asc" ]],
            columnDefs:[
                {"visible":false,"targets":[2]}
            ],
            language: opciones_idioma
        });
   }
    // Al seleccionar un responsable se seleccionarán/deseleccionarán todos los proyectos de los que es responsable
    $(".checkbox_responsable").on("change",function(){
        projectes_de_responsable(this);
    });

///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////

   if($(".table_llista_despeses")){// DESPESES
       $(".table_llista_despeses").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'de_date', targets: 0 }
            ],
            language: opciones_idioma
        });
    }

   if($(".table_llista_ingresos")){// INGRESOS
       $(".table_llista_ingresos").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'de_date', targets: 0 }
            ],
            language: opciones_idioma
        });
    }

//   if($(".table_llista_dades")){// DESPESES
//       $(".table_llista_dades").DataTable({
//            scrollY:        '60vh',
//            scrollCollapse: true,
//            paging:         false,
//            autowidth:      true,
////            columnDefs: [
////                { type: 'de_date', targets: 0 }
////            ],
//            language: opciones_idioma
//        });
//    }

////////////////////////////
});


function projectes_de_responsable(chk){
    var val = table_responsables.cell(table_responsables.row(".selected").index(),2).data();
    table_projectes.rows().every(function(rowidx,tableloop,rowloop){
        if(table_projectes.cell(rowidx,4).data()==val)
            $(table_projectes.row(rowidx,0).node()).find(":checkbox").prop("checked",$(chk).is(':checked'));
    });
//    console.log(table_responsables.cell(rowidx,2).data());
}