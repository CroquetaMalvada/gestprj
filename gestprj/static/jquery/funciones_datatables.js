$(document).ready(function(){
    var table = $("#centres_participants").DataTable({
        scrollY:        '50vh',
        scrollCollapse: true,
        paging:         false,
    });
    $("#centres_participants").DataTable().columns.adjust();

    $('#centres_participants tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );

    $('#eliminar_campo').click( function () {
        table.row('.selected').remove().draw( false );
    });

});

