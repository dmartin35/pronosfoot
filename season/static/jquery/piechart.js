createPieChart = function(container,data,mode,colors){
    if (colors === undefined) colors: [];
    return new Highcharts.Chart(container, {
		chart: {

			plotBackgroundColor: null,
			plotBorderWidth: null,
			plotShadow: false,
			type: 'pie'
		},
        
		title: {
			text: null
		},

        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>',
            enabled: false,
        },

        credits: {
            enabled: false
        },
        /*
        legend: {
            enabled: true
        },
        */

		plotOptions: {
			pie: {
				allowPointSelect: true,
                cursor: 'pointer',
                animation: false,

                /*


                animation: true,
				dataLabels: {
					enabled: true,
					formatter: function() {
						if (mode == 'percent')
						{return this.point.name +' : '+ this.y + '%';}
						else {return this.point.name +' : '+ this.y;}
					}
				},
				*/
				dataLabels: {
					enabled: true,
					formatter: function() {
						if (mode == 'percent')
						{return this.point.name[0] +' : '+ this.y + '%';}
						else {return this.point.name[0] +' : '+ this.y;}
					}
				},
				showInLegend: true,
				colors: colors,
			}
		},
		
	    series: [{
			/*type: 'pie',*/
			data: data
		}]
	});
};
