import datetime
from django.core.management.base import BaseCommand

from tools.log import _log
from admin.daily.calendar import check_calendar
from admin.daily.endofseason import check_season_results
from admin.daily.results import check_results


class Command(BaseCommand):
    help = 'Execute daily tasks: monitor fixtures calendar & sets daily results'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        execute daily tasks: 
            - check fixtures calendar with LFP API
            - check results for matches of the day & sets players scores accordingly
            - check for end of season & sets end of season player results accordingly
        """
        _log('DAILY {}'.format(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))

        for methodcbk in [check_calendar, check_results, check_season_results]:
            try:
                methodcbk()
            except Exception as exc:
                _log('{}: {}'.format(methodcbk.__name__, exc))
