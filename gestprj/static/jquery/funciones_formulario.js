$(document).ready(function(){

    $("#id_data_inici_prj").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});
    $("#id_data_fi_prj").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false });
    $("#id_data_docum_web").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false });

    ///clicks
     $('.servsubv').click(function(e){
        actualizar_categorias($(this))
	 });

     $('#fin').click(function(e){
        habilitar_fecha_fi_prj();
	 });
	 $('#checkbox_docum_web').click(function(e){
        habilitar_fecha_es_docum_web();
	 });

	 $("#boton_guardar").click(function(e){

	 });
//    //ejecutar una vez al cargar la pagina
    actualizar_categorias($("#id_serv_o_subven .servsubv:checked").first());
    habilitar_fecha_fi_prj();
    if($("#id_es_docum_web").val()=='S')
      $("#checkbox_docum_web").attr("checked",true);

    habilitar_fecha_es_docum_web();

});

//aqui deberrá haber una función que cargue y comprueve el contenido al modificar el proyecto
function actualizar_categorias(ser_o_sub){
        var tipo = ser_o_sub.val();
        $("#id_categoria option").each(function(){
            $(this).attr("hidden",true);
            if($(this).attr("class")==tipo || $(this).attr("class")==3)
                $(this).removeAttr("hidden");
        });
        $("#id_categoria").val($("#id_categoria option:not([hidden])").first().val());
}

function habilitar_fecha_fi_prj(){
    if($("#fin").is(":checked")){
        $("#id_data_fi_prj").prop("disabled", false);
    }else{
        $("#id_data_fi_prj").prop("disabled", true);
        $("#id_data_fi_prj").val(null);
    }
}

function habilitar_fecha_es_docum_web(){
    if($("#checkbox_docum_web").is(":checked")){
        $("#id_es_docum_web").val("S");

        $("#id_data_docum_web").prop("disabled", false);
    }else{
        $("#id_es_docum_web").val("N");

        $("#id_data_docum_web").prop("disabled", true);
        $("#id_data_docum_web").val(null);
    }
}