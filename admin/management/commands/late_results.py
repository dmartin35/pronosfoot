import argparse
import datetime
from django.core.management.base import BaseCommand
from admin.daily.results import _check_results_date


def valid_date(s):
    """ convert string to datetime.date object - or raises invalid argument error """
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


class Command(BaseCommand):
    help = 'Manually checks the results for a past date'

    def add_arguments(self, parser):
        parser.add_argument('day', type=valid_date,
                            help='Date of the day as YYYY-MM-DD')

    def handle(self, *args, **options):
        """
        In some cases, whe the daily results script is executed by cron, 
        some results are not available yet on the LFP website
        This command is intended to manually trigger the results verification
        for a specific day
        """
        day = options['day']
        self.stdout.write('Checks late results for date {}'.format(day))
        _check_results_date(day)

