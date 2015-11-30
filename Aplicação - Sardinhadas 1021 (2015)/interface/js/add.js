/*
Diogo Daniel Soares Ferreira
Escuteiros - Praia da Barra, 2015
Aplicação para gestão de produtos das sardinhadas


Interface Web
*/


$(document).ready(function(){
	$("#newprod").ready(function(event){
        $("#addprod").click(function(){
            var name, price, check = true;
            $.getJSON( "/listProd",function (data) {
	            name = document.getElementById('prodnamein').value;
	            price = document.getElementById('prodpricein').value;
	            if (name.length == 0 || price.length == 0 ||  isNaN(price) || parseFloat(price)<0 || name.includes("(") || name.includes(")")) {
	                check = false;
	            }
	            
		        	for (var i=0;i<data.length; i++)
		            {	
		            	if(data[i].name===name){
		            		check = false;
		            	}
		            }
		            
	            
	            if (check == true) {
	                $.post("/newProd",
	                {
	                    name: name,
	                    price: price
	                },
	                function (data) {
	                    alert(data.message);
	                });
	            } else {
	                alert('Erro na inserção de um novo produto. Verifique se o produto já existe, ou se o preço é correto. O nome do produto não pode conter os carateres "(" ou ")".');
	            }
            });
        });
    });
});