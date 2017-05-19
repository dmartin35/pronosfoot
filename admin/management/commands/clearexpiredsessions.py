from django.core.management.base import BaseCommand
from tools.djangodb import executeRawSqlQuery


class Command(BaseCommand):
    help = 'Clear expired sessions'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        """
        delete sessions that expired at least one day ago
        
        For performance issues, directly executes the delete operation on database, 
        instead of using the django's builtin clearsessions command that uses the sessions models
        """
        sql = 'DELETE FROM `django_session` WHERE `expire_date` < DATE_SUB( CURDATE( ) , INTERVAL 0 DAY );'
        executeRawSqlQuery(sql)
