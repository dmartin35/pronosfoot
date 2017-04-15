"""
CALENDAR
"""
import calendar

__all__ = ['mycalendar','next_month','previous_month']

def monthcal(year,month):
    """
    returns the calendar for a given year and month
    """
    return calendar.monthcalendar(year,month)
    
def next_month(year,month):
    if month == 12:
        return (year+1,1)
    else:
        return (year,month+1)

def previous_month(year,month):
    if month == 1:
        return (year-1,12)
    else:
        return (year,month-1)
    
if __name__ == '__main__':
    print(next_month(2011,5) == (2011,6))
    print(next_month(2010,12) == (2011,1))
    
    print(previous_month(2011, 5) == (2011,4))
    print(previous_month(2011, 1) == (2010,12))
    
    print(monthcal(2011, 5))
    
    