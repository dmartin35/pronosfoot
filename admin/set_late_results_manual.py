"""
daily administration
1.check fixtures calendar
2.check fixtures results and calculate players forecasts results
3.check forecasts and send reminder mail
4.check end of season and calculate season forecasts bonus
"""
import datetime

from admin.daily.results import _check_results_date
    
    
if __name__ == '__main__':
    d = datetime.date(2013,8,10)
    _check_results_date(d)

