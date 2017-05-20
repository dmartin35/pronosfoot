__author__ = 'dmartin'
from external.lfp_api import get_calendar

cal = get_calendar()
print(cal)


from external.lfp_api import get_score

res = get_score(5, 'Ajaccio', 'Monaco')
print(res)