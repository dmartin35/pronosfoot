import unittest

from external.ligue1_website_old import CALENDAR_URL
from external.ligue1_website_old.lfp_tools import escape_team_names
from tools.web import get_url_content


@unittest.skip('Skip test for parsing old LFP website')
class TestEscapeTeamNames(unittest.TestCase):

    def test_escape_question_mark_ical(self):
        """
        new ICS calendar available from LFP
        has ? character instead of accentuated capital letters

        This functions it to be able to fix this issue
        for all team names in the calendar
        :return:
        """

        ical = get_url_content(CALENDAR_URL)
        ical = escape_team_names(ical)
        self.assertFalse('?' in ical)

