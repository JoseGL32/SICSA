$(document).ready(function()
{   
    $('#motivo').hide();
    $('#motivo2').hide();
    $('#montoadelanto').hide();
    $("#t-montoad").removeAttr("required");

    var control = 1;
    var vaca = 1;

    $('#formpresta input[name=customRadio]').on('change', function() 
    {
            if (control == 1){
                $('#cuotas').hide();
                $('#inicio').hide();
                $('#final').hide();
                $('#pagar').hide();
                $('#montoprestamo').hide();
                $('#montoadelanto').show();
                $("#t-montopr").removeAttr("required");
                $("#t-cuota").removeAttr("required");
                $("#c-cuota").removeAttr("required");
                $("#inp-inicio").removeAttr("required");
                $("#inp-final").removeAttr("required");
                $("#t-abono").removeAttr("required");
                $('#formpresta').trigger("reset");
                $("#rbtAdelanto").prop("checked", true);
                control = control - 1;
            }
            else if(control == 0)
            {
                $('#cuotas').show();
                $('#inicio').show();
                $('#final').show();
                $('#pagar').show();
                $('#montoadelanto').hide();
                $('#montoprestamo').show();
                $("#t-montoad").removeAttr("required");
                $("#t-cuota").attr("required", true);
                $("#t-montopr").attr("required", true);
                $("#c-cuota").attr("required", true);
                $("#inp-inicio").attr("required", true);
                $("#inp-final").attr("required", true);
                $("#t-abono").attr("required", true);
                $('#formpresta').trigger("reset");
                $("#rbtPrestamo").prop("checked", true);
                control = control + 1;
            }
     });

     $('#formvaca input[name=marker]').on('change', function() 
    {
        if($("#otro").is(':checked')) {  
            $('#motivo').show();
            $("#motivo1").prop("required", true);
        } else {  
            $('#motivo').hide();
            $('#motivo1').removeAttr("required");
        } 
     });

     $('#formvia input[name=marker]').on('change', function() 
    {
        if($("#otro1").is(':checked')) {  
            $('#motivo2').show();
            $("#motivo3").prop("required", true);
        } else {  
            $('#motivo2').hide();
            $('#motivo3').removeAttr("required");
        } 
     });

     $( "#formpresta" ).submit(function( event ) {
        $("#cod").removeAttr("disabled");
        $("#nombres").removeAttr("disabled");
        $("#apellidos").removeAttr("disabled");
        $("#ced").removeAttr("disabled");
        $("#t-abono").removeAttr("disabled");

        var salario = $("#sal").val();
        var mon = $("#t-montopr").val();
        var cuotas = Math.trunc(mon / (salario * 0.3));
        cuotas = cuotas + 1;

        $("#c-cuota").val(cuotas);
        var total = mon / cuotas;
        $('#t-abono').val(total.toFixed(2));
      });

      $( "#formvaca" ).submit(function( event ) {
        $("#cod").removeAttr("disabled");
        $("#nombres").removeAttr("disabled");
        $("#apellidos").removeAttr("disabled");
      });

      $( "#formepp" ).submit(function( event ) {
        $("#cod").removeAttr("disabled");
        $("#nombres").removeAttr("disabled");
        $("#apellidos").removeAttr("disabled");
      });

      $("#formvia").submit(function( event ) {
        $("#cod").removeAttr("disabled");
        $("#nombres").removeAttr("disabled");
        $("#apellidos").removeAttr("disabled");
      });


    $('#vermontoprestamo').click(function(){
        $("#ver-montopr").removeAttr("disabled");
    });

    $('#vercuotas').click(function(){
        $("#ver-cuota").removeAttr("disabled");
    });

    $('#verconcepto').click(function(){
        $("#ver-concepto").removeAttr("disabled");
    });

    $('#verinicio').click(function(){
        $("#ver-inicio").removeAttr("disabled");
    });

    $('#verfinal').click(function(){
        $("#ver-final").removeAttr("disabled");
    });

    $('#vermontoad').click(function(){
        $("#ver-montoad").removeAttr("disabled");
    });

    $('#verconceptoad').click(function(){
        $("#ver-conceptoad").removeAttr("disabled");
    });

	$("#c-cuota").blur(function() 
    {
		var salario = $("#sal").val();
        var mon = $("#t-montopr").val();
        var cuotas = Math.trunc(mon / (salario * 0.3));
        cuotas = cuotas + 1;
        var cuo = $("#c-cuota").val();
        
        if (cuo < cuotas)
        {
            alert('El mínimo de cuotas disponible es: '+ cuotas);
            $("#c-cuota").val(cuotas);
            var cuo = $("#c-cuota").val();
        }

        var total = mon / cuo;
	    $('#t-abono').val(total.toFixed(2));
        //alert('si entro');
	});

    $("#t-montopr").blur(function() 
    {
        var salario = $("#sal").val();
        var mon = $("#t-montopr").val();
        var cuotas = Math.trunc(mon / (salario * 0.3));
        cuotas = cuotas + 1;

        $('#c-cuota').attr('min', cuotas);
        $("#c-cuota").val(cuotas);

        var cuo = $("#c-cuota").val();
        //alert('monto '+ mon);
        var total = mon / cuo;
        $('#t-abono').val(total.toFixed(2));
        mon = Number(mon);

        //alert('salario '+ salario);
        if (mon > salario)
        {
            alert('No puedes solicitar mas de: '+ salario);
            $('#t-montopr').val(0);
            $('#c-cuota').val(0);
            $('#t-abono').val(0);
        }

	});

    //Scripts para el ver y modificar solicitudes

    $("#ver-cuota").blur(function() 
    {
		var salario = $("#ver-sal").val();
        var mon = $("#ver-montopr").val();
        var cuotas = Math.trunc(mon / (salario * 0.3));
        cuotas = cuotas + 1;
        var cuo = $("#ver-cuota").val();
        
        if (cuo < cuotas)
        {
            alert('El mínimo de cuotas disponible es: '+ cuotas);
            $("#ver-cuota").val(cuotas);
            var cuo = $("#ver-cuota").val();
        }

        var total = mon / cuo;
	    $('#ver-abono').val(total.toFixed(2));
        //alert('si entro');
	});

    $("#ver-montopr").blur(function() 
    {
        var salario = $("#ver-sal").val();

        var mon = $("#ver-montopr").val();
        var cuotas = Math.trunc(mon / (salario * 0.3));
        cuotas = cuotas + 1;

        $('#ver-cuota').attr('min', cuotas);
        $("#ver-cuota").val(cuotas);

        var cuo = $("#ver-cuota").val();
        //alert('monto '+ mon);
        var total = mon / cuo;
        $('#ver-abono').val(total.toFixed(2));
        mon = Number(mon);

        //alert('salario '+ salario);
        if (mon > salario)
        {
            alert('No puedes solicitar mas de: '+ salario);
            $('#ver-montopr').val(0);
            $('#ver-cuota').val(0);
            $('#ver-abono').val(0);
        }
	});

    $("#actpres").submit(function( event ) {
        $("#ver-montopr").removeAttr("disabled");
        $("#ver-cuota").removeAttr("disabled");
        $("#ver-concepto").removeAttr("disabled");
        $("#ver-inicio").removeAttr("disabled");
        $("#ver-final").removeAttr("disabled");
        $("#ver-abono").removeAttr("disabled");
        $("#ver-montoad").removeAttr("disabled");
        $("#ver-conceptoad").removeAttr("disabled");
        $(".custom-control-input").removeAttr("disabled");

        var salario = $("#ver-sal").val();
        var mon = $("#ver-montopr").val();
        var cuotas = Math.trunc(mon / (salario * 0.3));
        cuotas = cuotas + 1;

        $("#ver-cuota").val(cuotas);
        var total = mon / cuotas;
        $('#ver-abono').val(total.toFixed(2));
      });
});