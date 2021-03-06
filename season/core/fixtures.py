"""
MATCHES LIST AND RESULTS
"""
from season.models import Fixture
from tools.utils import distinct
import datetime
from django.db.models import Count
import calendar
from external.odds import get_odds
from django.db.models import Q

__all__ = ['fixtures','fixturesDays','fixuresDaysForMonth',
           'countFixuresPerDayForMonth','fixturesDaysAndWeeksForMonth',
           'fixturesOfTheDay','fixtureTeams','isFixtureValid','hasFixtureStarted', 'isFixtureFinished',
           'getFixture', 'get_fixture_odds', 'get_team_fixtures']

def fixtures(week):
    """
    return the list of fixtures (with results if available) 
    for the given week 
    """
    #gets the fixtures and list of days for the fixtures of the week 
    return Fixture.objects.filter(week=week).order_by('day', 'hour', 'team_a').all()

def fixturesDays(week):
    """
    returns the list of days for fixtures to be played for given week
    """
    return distinct([f.day for f in Fixture.objects.filter(week=week).order_by('day').all()])

def fixuresDaysForMonth(year,month):
    """
    returns the list of match days for a given month
    """
    last_day = calendar.monthrange(year, month)[1]
    return distinct([f.day for f in Fixture.objects.filter(day__gte=datetime.date(year, month, 1),day__lte=datetime.date(year, month, last_day)).order_by('day').all()])

def countFixuresPerDayForMonth(year,month):
    """
    returns the number of matches for each day of the month; and the week of each match
    """
    last_day = calendar.monthrange(year, month)[1]
    return Fixture.objects.filter(day__gte=datetime.date(year, month, 1),day__lte=datetime.date(year, month, last_day)).values('day').annotate(count=Count('day')).order_by('day')

def fixturesDaysAndWeeksForMonth(year,month):
    """
    returns a dict containing day number as keys and fixture week number as value
    for each fixture of the given month  
    """
    days_to_week = {}
    for day in fixuresDaysForMonth(year,month):
        days_to_week[day.day] = Fixture.objects.filter(day=day).order_by('week').all()[0].week
    return days_to_week

def fixturesOfTheDay(day):
    """
    returns the list of fixtures of a specific day
    """
    return Fixture.objects.filter(day=day).all()

def fixtureTeams(fixture_id):
    """
    returns the home and away team names of the fixture
    """
    fixture = Fixture.objects.get(id=fixture_id)
    return {'team_a':fixture.team_a.name,'team_b':fixture.team_b.name}

def isFixtureValid(fixture_id):
    """
    check whether fixture id is valid in the DB
    """
    try:
        Fixture.objects.get(id=fixture_id)
    except Fixture.DoesNotExist:
        return False
    else:
        return True

def hasFixtureStarted(fixture_id):
    """
    indicates whether the fixture has started yet
    """
    currenttime = datetime.datetime.now()
    fixture = Fixture.objects.get(id=fixture_id)
    
    #indicates whether forecast can still be set - before match start time
    fixturetime = datetime.datetime(fixture.day.year,
                                    fixture.day.month,
                                    fixture.day.day,
                                    fixture.hour.hour,
                                    fixture.hour.minute,
                                    fixture.hour.second,
                                    fixture.hour.microsecond)
    if currenttime >= fixturetime:
        return True
    else:
        return False


def isFixtureFinished(fixture_id):
    """
    indicates whether a fixture is finished ie. when final score is filled in
    :param fixture_id:
    :return: boolean
    """
    fixture = Fixture.objects.get(id=fixture_id)
    return fixture.score_a is not None and fixture.score_b is not None


def getFixture(fixture_id):
    """ return the fixure for given ID, or None if not found """
    try:
        return Fixture.objects.get(id=fixture_id)
    except Fixture.DoesNotExist:
        return None


def get_fixture_odds(fixture_id):
    """
    returns the Odds for the given fixture - returns None if odds are not found (ie. probably too early) 
    :param fixture_id: 
    :return: namedtuple Odds
    """
    try:
        fixture = Fixture.objects.get(id=fixture_id)
        all_odds = get_odds()
        return all_odds.get((fixture.team_a.name, fixture.team_b.name))
    except Fixture.DoesNotExist:
        return None


def get_team_fixtures(team_id):
    """
    returns all fixtures for a team
    :param team_id:
    :return:
    """
    return Fixture.objects.filter(Q(team_a=team_id) | Q(team_b=team_id)).order_by('week')
