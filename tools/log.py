"""
LOGGING MODULE
"""
from django.conf import settings

from tools.file import write_file_line

def _log(str):
    """
    wrapper to log into log file
    """
    write_file_line(settings.LOG_FILE, str)