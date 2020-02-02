import unittest
from unittest import mock
import logging
logging.basicConfig()

from external import SCORE_URL
from external.lfp_api import get_score, get_calendar
from tools.web import get_url_content as _url_download
from . import TEST_LFP_TEAM_MAP_2017_2018

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
        self.assertEqual(len(calendar), 380)

        for key in ['date', 'time', 'team_a', 'team_b', 'week']:
            self.assertTrue(key in calendar[0])
