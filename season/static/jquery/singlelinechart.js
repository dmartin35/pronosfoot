createSingleLineChart = function(container,xdata,ydata,xlabel,ylabel,ymin,ymax,tickInterval,minorTickInterval,yreversed,xlabel_prefix,ylabel_suffix)
{
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
			minorTickInterval: minorTickInterval,
			min: ymin,
			max: ymax,
			startOnTick: false,
			endOnTick: false,
			allowDecimals: false,
			reversed : yreversed,
			showLastLabel: false,
			showFirstLabel: false
		},
			
		plotOptions: {
			line: {
				allowPointSelect: false,
                enableMouseTracking : true,
                animation: false,
				dataLabels: {
					enabled: false
				}
			}
		},
		
		tooltip: {
			formatter: function() {
				var str = '';
				if (xlabel_prefix != undefined)
				{
					str+= xlabel_prefix + ' ';
				} 
				str+= this.x +' : '+ this.y;
				if (ylabel_suffix != undefined)
				{
					if (ylabel_suffix instanceof Array)
					{
						if ( (this.y) < ylabel_suffix.length)
						{
							str += ' ' + ylabel_suffix[this.y-1];
						}else
						{
							str += ' ' + ylabel_suffix[ylabel_suffix.length-1];
						}
					}else
					{
						str += ' '+ ylabel_suffix;
					}
				}
				return str;
			}
		},
		
		series: [{
			type: 'line',
			data: ydata
		}]
	});
};