import datetime
from django.core.management.base import BaseCommand

from tools.log import _log
from admin.daily.calendar import check_calendar
from admin.daily.endofseason import check_season_results
from admin.daily.results import check_results


class Command(BaseCommand):
    help = 'Execute match results tasks: sets daily results (closest to end of game with cron)'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        This will be executed multiple times on weekend (fri-sat-sun) days by cron
        0 15,17,19,21,23 * * 0,5,6
        in order to get results as soon as game has ended and set players scores

        it will be fallback by the daily command (that will check results once end of day)
        """
        _log('RESULTS {}'.format(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))

        for methodcbk in [check_results]:
            try:
                check_results()
            except Exception as exc:
                _log('{}: {}'.format(methodcbk.__name__, exc))
