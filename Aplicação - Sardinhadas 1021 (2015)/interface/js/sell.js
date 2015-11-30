/*
Diogo Daniel Soares Ferreira
Apoio de Luís Davide Leira
Escuteiros - Praia da Barra, 2015
Aplicação para gestão de produtos das sardinhadas


Interface Web
*/

    
$('#userM').bind('input', function() { 
    troco();
});

$(document).ready(function(){

    $.getJSON( "/listProd",function (data) {
        for (var i=0;i<data.length; i++)
        {
            //$('#sellallprod').append('<td style="text-align: center" id="'+data[i].id+'n">'+data[i].name+'</td><td style="text-align: center" id="'+data[i].id+'p">'+data[i].pric+'</td><td style="text-align: center"><div class="box"><input id="qty'+data[i].id+'" value="0" disabled="disabled"/><button id="down" onclick="modify_qty(-1,'+data[i].id+','+data[i].pric+')">-1</button><button id="up" onclick="modify_qty(1,'+data[i].id+','+data[i].pric+')">+1</button></div></td>');
            $('#sellallprod').append('<div class="box" style="float:left;margin: 10px 10px 10px;border: 3px solid black;"><h5 style="text-align:center;"><b id="'+data[i].id+'n">'+data[i].name+'</b></h5><h6 style="text-align:center;" id="'+data[i].id+'p">'+data[i].pric+' euro(s)</h6><input id="qty'+data[i].id+'" value="0" disabled="disabled" style="display:flex;"><button id="down" onclick="modify_qty(-1, '+data[i].id+','+data[i].pric+')" style="float:left;margin-left:10px;">-1</button><button id="up" onclick="modify_qty(1,'+data[i].id+' , '+data[i].pric+')" style="float:right;margin-right:10px;">+1</button></div>');
        }
        
    });

    $("#finalize").click(function() {
        finalize()

    });


});



function modify_qty(val, id, price) {
    var qty = document.getElementById('qty'+id).value;

    if (qty==0 && val<0){
        return qty;
    } 
    var new_qty = parseInt(qty,10) + val;
                    
    if (new_qty < 0) {
        new_qty = 0;
    }
                    
    document.getElementById('qty'+id).value = new_qty;
    var total = document.getElementById('Total').innerHTML;
    document.getElementById('Total').innerHTML = Math.round((parseFloat(total) + parseFloat(val)*parseFloat(price)) * 100) / 100;
    troco();
    return new_qty;
}

function troco(){
    var troc = Math.round((document.getElementById('userM').value - parseFloat(document.getElementById('Total').innerHTML)) * 100) / 100;
    if (troc<0){
        document.getElementById('Troco').innerHTML = 0;
    }
    else{
        document.getElementById('Troco').innerHTML = troc;
    }

}

function finalize(){
    var len = 0;
    var data2;
    $.getJSON( "/listProd",function (data) {
        data2 = data.length;
        for (var i=0;i<data.length; i++)
        {
            if (document.getElementById('qty'+data[i].id).value!=0){
                prod = document.getElementById(data[i].id+'n').innerHTML;
                quan = document.getElementById('qty'+data[i].id).value;
                price = quan*document.getElementById(data[i].id+'p').innerHTML.split(" ")[0];
                $.getJSON("/sellProd",{prod: prod, quan: quan, price: price},function (data) {
                    len = len+1;
                    if(len===data2){
                        alertandreload();
                    }
                });
            }
            else{
                data2 = data2-1;
            }
        }
    });

    $.getJSON( "/addClient",function (data) {

    });

}

function alertandreload(){

    alert("Produtos vendidos com sucesso!");
    location.reload();
}