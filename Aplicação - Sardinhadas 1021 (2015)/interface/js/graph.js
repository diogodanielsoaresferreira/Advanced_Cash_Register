/*
Diogo Daniel Soares Ferreira
Escuteiros - Praia da Barra, 2015
Aplicação para gestão de produtos das sardinhadas


Interface Web
*/


$(document).ready(function(){
   

    var j=0;
    $.getJSON( "/getDays",function (data) {
        for (var i=0;i<data.length; i++)
        {
            j+=1;
            $('#daysform').append('<option id='+data[i].day+'>'+data[i].day+'</option>');
        }
        $('#daysform').append('<option id=all>Todos os dias</option>');
    });
    
    $("#day").click(function(){
        var luc = [];
        var prod = [];
        var quant = [];
        $("#container").html("");
        $("#soldprod").html("");
        $('#persons').html("");
        $.getJSON( "/getLucDay",{day: document.getElementById('daysform').value},function (data) {
            $.getJSON( "/getC",{day: document.getElementById('daysform').value},function (data) {
                $('#persons').append("<b>Pessoas atendidas: "+data[0].Pessoas+"</b>");
                if (document.getElementById('daysform').value === "Todos os dias"){
                    $('#persons').append("<br><b>Média de pessoas atendidas por dia: "+Math.round((data[0].Pessoas/j)*1000)/1000+"</b>");
                }
            });
            var quan = 0;
            var pric = 0;
            $('#soldprod').append('<table style="width:100%;"><tr><th style="text-align: center;width:30%;">Produto</th><th style="text-align: center;width:30%;">Quantidade vendida</th><th style="text-align: center;width:30%;">Dinheiro recebido (euros)</th></tr>');
            for (var i=0;i<data.length; i++)
            {
                quan += parseFloat(data[i].quant);
                pric += parseFloat(data[i].price);
                $('#soldprod').append('<tr style="width:100%"><td style="text-align: center;">'+data[i].prod+'</td><td style="text-align: center; ">'+data[i].quant+'</td><td style="text-align: center;padding-right:160px;padding-left:160px;">'+data[i].price+'</td></tr>');
                luc[i]=parseFloat(data[i].quant);
                quant[i]=parseFloat(data[i].price);
                prod[i]=data[i].prod;
            }
            $('#soldprod').append('<tr style="width:100%"><td style="text-align: center;">'+'<b>Total</b>'+'</td><td style="text-align: center; "><b>'+quan+'</b></td><td style="text-align: center;"><b>'+Math.round(pric*100)/100+'</b></td></tr>');
            $('#soldprod').append('</table>');
             // Create the chart
            $('#container').highcharts({
                chart: {
                    type: 'column',
                    backgroundColor: '#FFFFFF',
                    margin: 75,
                    options3d: {
                        enabled: true,
                        alpha: 10,
                        beta: 25,
                        depth: 70
                    }
                },
                
                title: {
                    text: 'Dinheiro recebido de cada produto vendido'
                },
                subtitle: {
                    text: 'Escuteiros Praia da Barra - Sardinhadas 2015'
                },
                plotOptions: {
                    column: {
                        depth: 25
                    }
                },
                xAxis: {
                    categories: prod
                },
                yAxis: {
                    title: {
                        text: 'Preço (euros)'
                    }
                },
                series: [{
                    name: 'Dinheiro recebido (em euros)',
                    data: luc
                }]
            });

            $('#container2').highcharts({
                chart: {
                    type: 'column',
                    backgroundColor: '#FFFFFF',
                    margin: 75,
                    options3d: {
                        enabled: true,
                        alpha: 10,
                        beta: 25,
                        depth: 70
                    }
                },
                
                title: {
                    text: 'Quantidade de vendas de cada produto'
                },
                subtitle: {
                    text: 'Escuteiros Praia da Barra - Sardinhadas 2015'
                },
                plotOptions: {
                    column: {
                        depth: 25
                    }
                },
                xAxis: {
                    categories: prod
                },
                yAxis: {
                    title: {
                        text: 'Número de vendas do produto'
                    }
                },
                series: [{
                    name: 'Quantidade',
                    data: quant
                }]
            });
        });
    });
});