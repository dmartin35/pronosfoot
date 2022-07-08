from django.core.management.base import BaseCommand
from admin.daily.results import check_missed_results



class Command(BaseCommand):
    help = 'Manually checks the missed results in the past'


    def handle(self, *args, **options):
        count = check_missed_results()
        print(count, "missed results")


