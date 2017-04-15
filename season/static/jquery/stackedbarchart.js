/**
 * Create a 100% stacked bar chart
 */
 
createStackedBarChart = function(container, series)
{
	return new Highcharts.Chart({
		chart: {
			renderTo: container,
			type: 'bar',
			plotShadow: false,
			
		},
		
		title: {
			text: null
		},
        
        credits: {
            enabled: false
        },
        
        legend: {
            enabled: true,
            reversed: true,
            
        },
		
		xAxis:{
			labels: {
				enabled: false
			},
		    lineWidth: 0,
		    minorGridLineWidth: 0,
		    lineColor: 'transparent',
		    minorTickLength: 0,
		    tickLength: 0
		},
		yAxis: {
			min: 0,
			max: 100,
			labels: {
				enabled: false
			},
			title: {
				text: null
			},
			gridLineWidth: 0,
			
		},
		tooltip: {
			enabled: false,
		},
		
		plotOptions: {
			series: {
				stacking: 'normal',
				animation: false,
				events: {
					click: false,
					legendItemClick: false,
				},
				enableMouseTracking: false,
				dataLabels: {
                    enabled: true,
                    color: 'white',
                    align: 'center',
                    formatter: function() {
                    	if (this.y > 0)
                    	{
							return '' + this.y +'%';
						}
						else{
							return '';
						}
					}
                }
			}
		},
		
		series: series,
	});
};