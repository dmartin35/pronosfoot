from django.core.management.base import BaseCommand

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
        # create an save in DB a new table entry
        Table(team=team, week=0, points=0,
              win=0, draw=0, lose=0,
              goal_for=0, goal_against=0).save()


def init_calendar():
    """
    initialize the entire season fixtures in DB from calendar
    """
    lfp_cal = get_calendar()
    for idx, fixt_dict in enumerate(lfp_cal):

        # create and save in DB a new fixture entry
        # !! since ical does not contains any information
        # about the week of a game, we consider at first cal init
        # that all games per week are listed in right order !!
        week = idx // 10 + 1
        Fixture(week=week,
                team_a=Team.objects.get(name=fixt_dict['team_a']),
                team_b=Team.objects.get(name=fixt_dict['team_b']),
                day=fixt_dict['date'],
                hour=fixt_dict['time']).save()


class Command(BaseCommand):
    help = 'Preapare new season: populates the database with initial data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        prepare all data model for a new season

        - get the list of teams from LFP
        - initialize the teams DB 
        - initialize the league table DB for each team

        - get the calendar from LFP
        - initialize the fixtures DB
        """
        self.stdout.write('Populates teams...')
        init_teams()
        self.stdout.write('OK')

        self.stdout.write('Initializes league table...')
        init_table()
        self.stdout.write('OK')

        self.stdout.write('Register fixtures for entire season...')
        init_calendar()
        self.stdout.write('OK')











