# """
# daily administration
# 1.check fixtures calendar
# 2.check fixtures results and calculate players forecasts results
# 3.check forecasts and send reminder mail
# 4.check end of season and calculate season forecasts bonus
# """
# import datetime
#
# from tools.log import _log
# from admin.daily.calendar import check_calendar
# from admin.daily.endofseason import check_season_results
# #from admin.daily.reminder import check_forecasts
# from admin.daily.results import check_results
#
#
# if __name__ == '__main__':
#
#     _log('DAILY {}'.format(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
#
#     for methodcbk in [check_calendar, check_results, check_season_results]:
#         try:
#             methodcbk()
#         except Exception as exc:
#             _log('{}: {}'.format(methodcbk.__name__, exc))
