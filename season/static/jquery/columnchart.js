createColumnChart = function(container,xdata,ydata,xlabel,ylabel,tickInterval){
    return new Highcharts.Chart({
		chart: {
            renderTo: container,
			plotBackgroundColor: null,
			plotBorderWidth: null,
			plotShadow: false,
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
        xAxis: {
			categories: xdata,
			title: {
				text: xlabel
			},
		},
		yAxis: {
			title: {
				text: ylabel
			},
			tickInterval: tickInterval,			
			startOnTick: false,
			endOnTick: false,
			stackLabels: {
				enabled : false
			},
			labels: {
				enabled: true
			}
		},
		plotOptions: {
			series: {
				allowPointSelect: false,
                enableMouseTracking : false,
                animation: false,
                dataLabels: {
					enabled: true,
					color: 'gray',
					formatter: function() {
						if (this.y == 0) {
							return '';
						}else if (this.y > 0){
							return '+'+this.y;
						}else{
							return this.y;
						}
					}
				}
			}
		},
		series: [{
			type: 'column',
			data: formatDataSerie(ydata)
		}]
	});
};

/**
* assign specific color to negative-positive value
*/
formatDataSerie = function(data){
	var res = [];
	for (idx in data)
	{
		var val = data[idx];
		var dict = {};
		dict['y'] = val;
		if (val <0)
		{
			dict['color'] = '#d00000';
		}else{
			dict['color'] = '#396338';
		}
		res[idx] = dict;
	}
	return res;
};
