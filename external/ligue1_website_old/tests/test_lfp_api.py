import os
import unittest
from unittest import mock
import logging
logging.basicConfig()

from external.ligue1_website_old import SCORE_URL
from external.ligue1_website_old.lfp_api import get_score, get_calendar
from tools.web import get_url_content as _url_download
from . import TEST_LFP_TEAM_MAP_2017_2018, TEST_LFP_TEAM_MAP_2020_2021


@unittest.skip('Skip test for parsing old LFP website')
class TestLFPApi(unittest.TestCase):

    @mock.patch.dict('external.lfp_results.LFP_TEAM_MAP', TEST_LFP_TEAM_MAP_2017_2018)
    @mock.patch('external.lfp_api.get_url_content')
    def test_get_scores(self, mock_url_content):
        """
        This test ensures LFP website does not change its html structure over time
        by checking some known results
        """

        mock_url_content.return_value = _url_download(SCORE_URL % ('2017-2018', 1))

        self.assertEqual(get_score(1, 'Monaco', 'Toulouse'), (3, 2))
        self.assertEqual(get_score(1, 'Troyes', 'Rennes'), (1, 1))
        self.assertEqual(get_score(1, 'Marseille', 'Dijon'), (3, 0))

    def test_download_calendar(self):
        """
        This test is to ensure LFP calendar is still available for download
        and the ICAL parsing is not broken over time
        """
        calendar = get_calendar()
        # self.assertTrue(len(calendar) >= 380)  # 380 with 20 clubs
        self.assertTrue(len(calendar) >= 306)  # is now X with 18 clubs
        # NB: greater for duplicated entries in ical for postponed/rescheduled matches

        for key in ['date', 'time', 'team_a', 'team_b', 'week']:
            self.assertTrue(key in calendar[0])

    @mock.patch.dict('external.lfp_results.LFP_TEAM_MAP', TEST_LFP_TEAM_MAP_2020_2021)
    @mock.patch('external.lfp_api.get_url_content')
    def test_ical_has_no_unescaped_question_mark(self, mock_url_content):
        fpath = os.path.join(os.path.dirname(__file__), 'LFP-D1-2020-2021.ics')
        with open(fpath, 'r') as ics:
            mock_url_content.return_value = ics.read()

        invalid = set()
        calendar = get_calendar()
        # ensure no unexpected '?' are left/forgotten in team names
        for fixture in calendar:
            for team in ['team_a', 'team_b']:
                if '?' in fixture[team]:
                    invalid.add(fixture[team])

        # check that invalid set is empty
        self.assertEqual(invalid, set())
