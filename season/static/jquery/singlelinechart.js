createSingleLineChart = function(container,xdata,ydata,xlabel,ylabel,ymin,ymax,tickInterval,minorTickInterval,yreversed,xlabel_prefix,ylabel_suffix,yticks)
{
//console.log('container','xdata','ydata','xlabel','ylabel','ymin','ymax','tickInterval','minorTickInterval','yreversed','xlabel_prefix','label_suffix');
//console.log(container,xdata,ydata,xlabel,ylabel,ymin,ymax,tickInterval,minorTickInterval,yreversed,xlabel_prefix,ylabel_suffix);

	return new Highcharts.Chart({
		chart: {
		    type: 'line',
            renderTo: container,
			plotBackgroundColor: null,
			plotBorderWidth: null,
			plotShadow: false
		},
        
		title: {
			text: null
		},
        subtitle: {
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
			tickPositions: yticks,
			min: ymin,
			max: ymax,
			//minRange: 5,
			startOnTick: true,
			endOnTick: true,
			allowDecimals: false,
			reversed : yreversed,
			showLastLabel: true,
			showFirstLabel: true
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
			data: ydata
		}]
	});
};