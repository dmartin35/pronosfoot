"""
WEEKS MANAGEMENT
"""
from season.models import Fixture
from tools.utils import distinct
import datetime

WEEK_CLOSEST = 'closest'
WEEK_NEXT = 'next'
WEEK_LAST = 'last'

__all__ = ['WEEK_CLOSEST', 'WEEK_NEXT', 'WEEK_LAST', 'getWeekAuto', 'checkWeekValidity', 'getAllWeeks']

def getAllWeeks():
    """
    return the complete list of weeks available
    """
    return distinct([f.week for f in Fixture.objects.order_by('week').all()])

def getWeekAuto(date,mode):
    """
    returns the week from the given date depending 
    on the mode (next, last, closest)
    
    if no next week, returns the last available
    if no last week, returns the first available
    NB: there should always be a closest week
    """
    if mode == WEEK_CLOSEST:
        return _getClosestWeekAuto(date)
    elif mode == WEEK_NEXT:
        return _getNextWeekAuto(date)
    elif mode == WEEK_LAST:
        return _getLastWeekAuto(date)
    
def _getClosestWeekAuto(date):
    """
    returns the closest week to the given date
    """
    days = distinct([f.day for f in Fixture.objects.order_by('day').all()])
    closest_day = None
    
    if isinstance(date,str):
        (year,month,day) = date.split('-')
        date_dt = datetime.date(int(year),int(month),int(day))
        
        if days != []:
            closest_day = days.pop(0)
            
            for day in days:
                if abs(date_dt - day) < abs(date_dt - closest_day):
                    #new closest found
                    closest_day = day
    
    if not closest_day is None:
        #return the week of the first fixture whose day is the closest to given date
        return [f.week for f in Fixture.objects.filter(day=closest_day).all()].pop(0)
    
    #should not get here
    return None
    

def _getNextWeekAuto(date):
    """
    returns the next week following the given date
    if no more weeks, returns the last one available
    """
    #filter fixtures with greater or equal dates
    nextweek_fixture = [f for f in Fixture.objects.filter(day__gte=date).order_by('day').all()]
    if nextweek_fixture != []:
        return nextweek_fixture.pop(0).week
    else:
        #no more weeks after current day, 
        #use last available week for entire season
        last_fixture = [f for f in Fixture.objects.order_by('week').all()]
        if last_fixture != []:
            return last_fixture.pop().week
    
    #should not get here
    return None

def _getLastWeekAuto(date):
    """
    returns the last week depending on the current date
    if no previous week, returns the first one available
    """
    #filter fixtures with lower dates - get last item
    lastweek_fixture = [f for f in Fixture.objects.filter(day__lt=date).order_by('day').all()]
    if lastweek_fixture != []:
        return lastweek_fixture.pop().week
    else:
        #no more weeks before given date, 
        #use first available week for entire season
        first_fixture = [f for f in Fixture.objects.order_by('week').all()]
        if first_fixture != []:
            return first_fixture.pop(0).week
    
    #should not get here
    return None

def isWeekValid(week):
    """
    check the given week exists in the data base,
    i.e. a fixture exists for the specified week,
    """
    return Fixture.objects.filter(week=week).count() != 0

