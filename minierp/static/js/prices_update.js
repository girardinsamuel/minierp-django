// JavaScript Document
$("#id_acompteht").change(function(event) {
	var acompte= parseFloat($(this).val());
	var tva = parseFloat($('#id_tva option:selected').text());
	var dejaregle = acompte + acompte*tva*0.01
	$('#id_dejaregle').val(dejaregle.toFixed(2));
	$("#id_acomptettc").val(0.00);
	var ttc = parseFloat($("#id_prixttc").val());
	var dejaregle = parseFloat($("#id_dejaregle").val());
	var net=ttc-dejaregle;
	$("#id_netapayer").val(net.toFixed(2));
});

$("#id_acomptettc").change(function(event) {
	var acompte = parseFloat($(this).val());
	$("#id_acompteht").val(0.00);
	$('#id_dejaregle').val(acompte.toFixed(2));
	var ttc = parseFloat($("#id_ttc").val());
	var dejaregle = parseFloat($("#id_dejaregle").val());
	if ( ttc = 0 ) 
	{
		calculprixht();
	}
	else
	{
		calculprixttc();
	}
	
	var net=ttc-dejaregle;
	$('#id_netapayer').val(net.toFixed(2));
});

$("#id_prixht").change(function(event) {
	calculprixttc();
});
$("#id_prixttc").change(function(event) {
	calculprixht();
});



// function calculdejareglettc()
// {
// 	var acompte= parseFloat(document.getElementById("form").elements["acomptettc"].value);
// 	document.getElementById("form").elements["acompteht"].value =  0.00;
// 	document.getElementById("form").elements["dejaregle"].value =  acompte.toFixed(2);
// 	 var dejaregle = parseFloat(document.getElementById("form").elements["dejaregle"].value);
// 	var ttc = parseFloat(document.getElementById("form").elements["ttc"].value);
// 	if ( ttc = 0 ) 
// 	{
// 		calculprixht();
// 	}
// 	else
// 	{
// 		calculprixttc();
// 	}
	
// 	var net=ttc-dejaregle;
// 	document.getElementById("form").elements["netapayer"].value =  net.toFixed(2);
// }

function calculprixht()
{
	var ttc = parseFloat($("#id_prixttc").val());
	var tva = parseFloat($('#id_tva option:selected').text());
	var dejaregle = parseFloat($("#id_dejaregle").val());
	var prixht = ttc/(1+tva*0.01);
	var parttva = ttc-prixht;
	var net = ttc-dejaregle;
	$("#id_prixht").val(prixht.toFixed(2));
	$("#id_parttva").val(parttva.toFixed(2));
	$("#id_netapayer").val(net.toFixed(2));
}


function calculprixttc()
{
	var ht = parseFloat($("#id_prixht").val());
	var tva = parseFloat($('#id_tva option:selected').text());
	var dejaregle = parseFloat($("#id_dejaregle").val());
	var parttva = ht*tva*0.01;
	var prixttc = ht + parttva;
	var net = prixttc-dejaregle;
	
	$("#id_prixttc").val(prixttc.toFixed(2));
	$("#id_parttva").val(parttva.toFixed(2));
	$("#id_netapayer").val(net.toFixed(2));
}

function init_prices()
{
	$("#id_prixht").val(0.00);
	$("#id_acompteht").val(0.00);
	$("#id_acomptettc").val(0.00);
	$("#id_prixttc").val(0.00);
	$("#id_parttva").val(0.00);
	$("#id_dejaregle").val(0.00);
	$("#id_netapayer").val(0.00);
}