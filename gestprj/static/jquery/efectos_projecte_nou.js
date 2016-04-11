$(document).ready(function(){
    mostrar_menu("#contenedor_general");
    $("#general").parent("li").addClass("active");

    $("#general").click(function(){
        mostrar_menu("#contenedor_general");
        $(this).parent("li").addClass("active");
    });

    $("#personal").click(function(){
        mostrar_menu("#contenedor_personal");
        $(this).parent("li").addClass("active");
    });

    $("#finançament").click(function(){
        mostrar_menu("#contenedor_finançament");
        $(this).parent("li").addClass("active");
    });

    $("#pressupost").click(function(){
        mostrar_menu("#contenedor_pressupost");
        $(this).parent("li").addClass("active");
    });

    $("#justificacions").click(function(){
        mostrar_menu("#contenedor_justificacions");
        $(this).parent("li").addClass("active");
    });

});


function mostrar_menu(nombre){
$("#contenedor_general").hide();
$("#contenedor_personal").hide();
$("#contenedor_finançament").hide();
$("#contenedor_pressupost").hide();
$("#contenedor_justificacions").hide();

$("#general").parent("li").removeClass("active");
$("#personal").parent("li").removeClass("active");
$("#finançament").parent("li").removeClass("active");
$("#pressupost").parent("li").removeClass("active");
$("#justificacions").parent("li").removeClass("active");

$(nombre).show();
}