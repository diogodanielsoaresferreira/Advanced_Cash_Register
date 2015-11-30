/*
Diogo Daniel Soares Ferreira
Escuteiros - Praia da Barra, 2015
Aplicação para gestão de produtos das sardinhadas


Interface Web
*/

$(document).ready(function(){
	$("#showallprod").ready(function(event){
		$.getJSON( "/listProd",function (data) {
			$('#showallprod').append('<table style="width:100%;"><tr><th style="text-align: center;width:35%;">Nome</th><th style="text-align: center;width:35%;">Preço (Euro)</th><th style="text-align: center;width:8%;">Alterar</th><th style="text-align: center;width:7%;">Apagar</th></tr>');
			for (var i=0;i<data.length; i++)
			{
				$('#showallprod').append('<tr style="width:100%; padding: 5px;"><td style="text-align: center">'+data[i].name+'</td><td style="text-align: center">'+data[i].pric+'</td><td style="text-align: center"><button type="button" class="btn btn-warning" id="'+data[i].id+'p">Editar Preço</button></td><td style="text-align: center"><button type="button" class="btn btn-danger" id="'+data[i].id+'">Apagar</button></td></tr>');
				m ='#'+data[i].id.toString();
				m2 ='#'+data[i].id.toString()+"p";
				$(m).click(function() {
					pid=this.id;
					if (confirm("Deseja mesmo apagar este produto?") == true) {
					    $.getJSON("/delprod",{id: pid},function (data2) {
							location.reload();
							alert("Produto eliminado com sucesso!");
						});
					}

				});

				$(m2).click(function() {
					pid=this.id.substring(0, this.id.length-1);
					var price = prompt("Insira o novo preço:");
					if (price.length == 0 ||  isNaN(price) || parseFloat(price)<0) {
	                	alert("Preço inválido!");
	            	}
				    else {
				    	$.getJSON("/changePrice",{id: pid, price: price},function (data3) {
							location.reload();
							alert("Preço alterado com sucesso para "+price+" euros.");
						});
						
				    }

				});

			}
			$('#showallprod').append('</table>');
		});
	});

});
