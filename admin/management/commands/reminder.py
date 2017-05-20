from django.core.management.base import BaseCommand
from admin.daily.reminder_txt import check_forecasts

class Command(BaseCommand):
    help = 'Send reminder email to players that have not registered their forecasts'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        check_forecasts()
