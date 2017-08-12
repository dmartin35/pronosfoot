import os
import unittest
from unittest import mock
import logging
logging.basicConfig()

from external.lfp_results import parse_results_page
from . import TEST_LFP_TEAM_MAP


class TestLFPResults(unittest.TestCase):

    @mock.patch.dict('external.lfp_results.LFP_TEAM_MAP', TEST_LFP_TEAM_MAP)
    def test_parse_lfp_results(self):

        fpath = os.path.join(os.path.dirname(__file__), 'lfp_101_01.html')
        html = open(fpath, 'r').read()
        results = parse_results_page(html)

        self.assertNotEqual(results, None)
        self.assertEqual(len(results), 10)

        print(results)
        self.assertTrue({'team_a': 'Monaco', 'team_b': 'Toulouse', 'score_a': 3, 'score_b': 2} in results)
        self.assertTrue({'team_a': 'Troyes', 'team_b': 'Rennes', 'score_a': 1, 'score_b': 1} in results)
        self.assertTrue({'team_a': 'Marseille', 'team_b': 'Dijon', 'score_a': 3, 'score_b': 0} in results)
