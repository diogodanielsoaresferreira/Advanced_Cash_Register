/*
Diogo Daniel Soares Ferreira
Escuteiros - Praia da Barra, 2015
Aplicação para gestão de produtos das sardinhadas


Interface Web
*/

$(document).ready(function(){
    $.getJSON( "/listProd",function (data) {
        for (var i=0;i<data.length; i++)
        {
            $('#sellform').append('<option id='+data[i].pric+'>'+data[i].name+' ('+data[i].pric+' euros)'+'</option>');
        }
    });
    
    $("#devprod").click(function(){
        quan = document.getElementById('quan').value;
        if(!(quan % 1 === 0) || quan <= 0){
            alert("Quantidade no formato errado!");
        }
        
        else{
        	prod = document.getElementById('sellform').value.split("(")[0];
        	quan = (-1)*document.getElementById('quan').value;
        	price = quan*parseFloat(document.getElementById('sellform').value.split("(")[1]);

            $.getJSON("/sellProd",{prod: prod.substring(0, prod.length-1), quan: quan, price: price},function (data) {
                alert("Produto devolvido com sucesso!");
            });
        }
    });
    $("#delprod").click(function() {
		if (confirm("Deseja mesmo apagar todas as vendas?") == true) {
			$.getJSON("/delProd",function (data2) {
				location.reload();
				alert("Vendas apagadas com sucesso!");
			});
		}
	});
	
});