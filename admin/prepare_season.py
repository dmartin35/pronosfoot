"""
prepare all data model for a new season

- get the list of teams from LFP
- initialize the teams DB 
- initialize the league table DB for each team

- get the calendar from LFP
- initialize the fixtures DB
"""
import django
# mandatory call to make use of django in independent script
django.setup()

from external.lfp_api import get_teams
from external.lfp_api import get_calendar

from season.models import Team
from season.models import Table
from season.models import Fixture


def init_teams():
    """
    initialize the Teams DB 
    """
    for name in get_teams():
        # create and save in DB new team
        Team(name=name).save()

    
def init_table():
    """
    for each team in the DB, creates an entry in the Table table
    in order to initialize league table (week 0)
    """
    teams = Team.objects.all()
    for team in teams:
        # create an dsave in DB a new table entry
        Table(team=team,week=0,points=0,
              win=0,draw=0,lose=0,
              goal_for=0,goal_against=0).save()


def init_calendar():
    """
    initialize the entire season fixtures in DB from calendar
    """
    lfp_cal = get_calendar()
    for fixt_dict in lfp_cal:
        # create and save in DB a new fixture entry
        Fixture(week = fixt_dict['week'],
                team_a = Team.objects.get(name=fixt_dict['team_a']),
                team_b = Team.objects.get(name=fixt_dict['team_b']),
                day = fixt_dict['date'],
                hour = fixt_dict['time']).save()


if __name__ == '__main__':
    init_teams()
    init_table()
    init_calendar()

