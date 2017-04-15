createPieChart = function(container,data,mode){
    return new Highcharts.Chart({
		chart: {
            renderTo: container,
			plotBackgroundColor: null,
			plotBorderWidth: null,
			plotShadow: false
		},
        
		title: {
			text: null
		},
        
        credits: {
            enabled: false
        },
        
        legend: {
            enabled: false
        },
        
		tooltip: {
			enabled:false
		},
        
		plotOptions: {
			pie: {
				allowPointSelect: false,
                enableMouseTracking : false,
                animation: false,
				dataLabels: {
					enabled: true,
					formatter: function() {
						if (mode == 'percent')
						{return this.point.name +' : '+ this.y + '%';}
						else {return this.point.name +' : '+ this.y;}
					}
				}
			}
		},
		
	    series: [{
			type: 'pie',
			data: data
		}]
	});
};
