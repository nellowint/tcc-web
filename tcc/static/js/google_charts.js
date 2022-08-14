"use strict"

$(function() {
    google.charts.load('current', {packages: ['corechart', 'bar']});

    let jsonFeedback;
    let jsonSearch;

    getJson($('#url_feed'), function(response) {
        jsonFeedback = response;
        google.charts.setOnLoadCallback(drawFeedbackChart);
    });
    getJson($('#url_search'), function(response) {
        jsonSearch = response;
        google.charts.setOnLoadCallback(drawSearchChart);
    });

    function drawFeedbackChart() {
        $.each($('.vt-chart-feedback'), function(index) {
            if(isDefined(jsonFeedback)) {           
                let rows = [];
                let question = $(this).attr('data-title');

                Object.keys(jsonFeedback[question]).forEach(function(key,answerIndex) {
                    let row = [key, jsonFeedback[question][key]];
                    rows.push(row);
                });
                
                let options = {
                       title: question,
                       is3D: true,
                       chartArea: {left:15,width:"100%"},
                       width:360,
                       height:300};

                let axisTitle = {'x': 'Respostas', 'y': 'Porcentagem'};

                drawChart(axisTitle, rows, options, $(this)[0], 'PIE');
            }
        });
    }

    function drawSearchChart() {
        if(isDefined(jsonSearch)) {
            let rows = [];

            jsonSearch = {'Arroz Parboilizado Ideal 5 kg': 9, 'Linguicinha Sulita Toscana kg': 9, 'Chocolate Bis Sabores 26 g': 8, 'Cerveja Budweiser Long Neck 900 ml': 8, 'Café Tropeiro Extra Forte 500 g': 8, 'Farinha De Trigo Roseflor 5 kg': 8, 'Cerveja Skol 350 ml': 7, 'Lasanha Seara Sabores 600 g': 6, 'Vassoura Condor und': 6, 'Limpador Veja Perfumes 500 ml': 6, 'Cerveja Kaiser 350 ml': 5, 'Miolo de Alcatra Bovino kg': 4, 'Alcatra com Maminha kg': 4, 'Refresco Em Pó Trink Sabores 25 g': 4, 'Steinhaeger Double W 900 ml': 4, 'Pepino em Conserva LUCA Pote 300 g': 4, 'Ovos De Codorna Juréria 300 g': 4, 'Antisséptico Bucal Listerine Cool Mint Leve 500ml Pague 350 ml': 4, 'Açúcar Alto Alegre Refinado 5 kg': 4, 'Leite Condensado Italac 395 g': 3, 'Pizza Calabresa Congelada 680 g': 3, 'Chocolate Lacta Ao Leite 150 g': 3, 'Carvão Vegetal 2,95 kg': 3, 'Milho Predilecta Lata 200 g': 3, 'Filé Americano Bovino kg': 3, 'Molho Barbecue Hemmer 330 g': 3, 'Coxa Sobrecoxa Sem Dorso kg': 3, 'Chocolate Lacta BIS Oreo 26 g': 3, 'Leite Italac Integral 1 l': 3, 'Refrigerante SPRITE Garrafa 2 l': 3, 'Iogurte Frutirol 540 g': 2, 'Banana da Prata 1 kg': 2, 'Ovos Negosek vermelho 30 und': 2, 'Melancia kg': 2, 'Sabão em Pó Surf 1 kg': 2, 'Açai Frooty Natural 2 kg': 2, 'Pepino kg': 2, 'Cerveja Caracu Stout Ale Lata 350 ml': 2, 'Refresco em Pó Tang 25 g': 2, 'Queijo Mussarela Fatiado Tirol 150 g': 2, 'Saco de Gelo 3,5 kg': 2, 'Farinha de Trigo Tradicional QUALITÁ Pacote 1 kg': 1, 'Extrato de Tomate Fugini Sachê 190 g': 1, "Maionese HellMann's 500 g": 1, 'Maçã Fuji kg': 1, 'Suco de Soja Ades 1 l': 1, 'Laranja Pêra 1 kg': 1, 'Arroz Especial Tipo 1 Arbório URBANO Pacote 1 kg': 1, 'Laranja Lima QUALITÁ 2 kg': 1, 'Detergente Ype Clear 500 ml': 1, 'Tomate kg': 1, 'Creme Dental Colgate Tripla Ação 90 g': 1, 'Refrigerante COCA COLA Garrafa 2 l': 1, 'Leite Tirol Integral 1 l': 1, 'Suco de Uva Tinto Integral Garibaldi 1,5 l': 1, 'Refrigerante GLUB Guaraná Garrafa 2 l': 1, 'Pedra Sanitária Sani-all 35 g': 1, 'Uva bdj': 1, 'Doce de Leite Tirol 350 g': 1, 'Amaciante Comfort concentrado 1 l': 1, "Pera d'Anjou 500 g": 1, 'Laranja Navel 1 kg': 1, 'Mamão Papaya Aprox.450g und': 1, 'Abacaxi und': 1}
            
            Object.keys(jsonSearch).forEach(function(key,index) {
                let row = [key, jsonSearch[key]];
                rows.push(row);
            });

            let options = {
                width:600,
                height:300,
                legend: { position: "none" },
                bars: 'horizontal',
                axes: {
                    x: {
                        0: { side: 'bottom', label: 'Quantidade de acesso'}
                    }
                },
                bar: { groupWidth: "90%" }
            };

            let axisTitle = {'x': 'Produtos', 'y': 'Quantidade de acesso'};
            
            drawChart(axisTitle, rows.slice(0,10), options, $('.vt-chart-prod')[0], 'BAR');
        }
    }

    function drawChart(axisTitle, rows, options, element, chartType) {
        let data = new google.visualization.DataTable();
        data.addColumn('string', axisTitle.x);
        data.addColumn('number', axisTitle.y);
            
        data.addRows(rows);

        let chart;
        
        if(chartType == 'BAR') {
            chart = new google.charts.Bar(element);
            chart.draw(data, google.charts.Bar.convertOptions(options));
        } else {
            chart = new google.visualization.PieChart(element);
            chart.draw(data, options);
        }
    }

    function isDefined(variable) {
        if(typeof variable !== 'undefined') {
            return true;
        }
        return false;
    }

    function getJson(element, success) {
        let url = element.attr('data-url') + '?format=json';
        $.get(url, function(response) {
            success(response);
        });
    }
});