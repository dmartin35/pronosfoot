import os
import unittest
from unittest import mock
import logging
logging.basicConfig()

from external.ligue1_website_old.lfp_results import parse_results_page
from . import TEST_LFP_TEAM_MAP_2017_2018, TEST_LFP_TEAM_MAP_2019_2020


@unittest.skip('Skip test for parsing old LFP website')
class TestLFPResults(unittest.TestCase):

    @mock.patch.dict('external.lfp_results.LFP_TEAM_MAP', TEST_LFP_TEAM_MAP_2019_2020)
    def test_parse_lfp_results(self):

        fpath = os.path.join(os.path.dirname(__file__), 'lfp_2019-2020_01.html')
        html = open(fpath, 'r').read()
        results = parse_results_page(html)

        self.assertNotEqual(results, None)
        self.assertEqual(len(results), 10)

        self.assertTrue({'team_a': 'Monaco', 'team_b': 'Lyon', 'score_a': 0, 'score_b': 3} in results)
        self.assertTrue({'team_a': 'Brest', 'team_b': 'Toulouse', 'score_a': 1, 'score_b': 1} in results)
        self.assertTrue({'team_a': 'Lille', 'team_b': 'Nantes', 'score_a': 2, 'score_b': 1} in results)

    @mock.patch.dict('external.lfp_results.LFP_TEAM_MAP', TEST_LFP_TEAM_MAP_2019_2020)
    def test_parse_with_accented_characters(self):
        """
        Test LFP results with teams that have accented characters
        """

        fpath = os.path.join(os.path.dirname(__file__), 'lfp_2019-2020_01.html')
        html = open(fpath, 'r').read()
        results = parse_results_page(html)

        # Nimes i-circumflex is replaced with i
        self.assertTrue({'team_a': 'Paris', 'team_b': 'Nimes', 'score_a': 3, 'score_b': 0} in results)
        # Montpelier Herault e-acute is replaced with e
        self.assertTrue({'team_a': 'Montpellier', 'team_b': 'Rennes', 'score_a': 0, 'score_b': 1} in results)
        # Saint-Etienne capital e-acute is replaced with capital e
        self.assertTrue({'team_a': 'Dijon', 'team_b': 'Saint-Etienne', 'score_a': 1, 'score_b': 2} in results)

    @mock.patch.dict('external.lfp_results.LFP_TEAM_MAP', TEST_LFP_TEAM_MAP_2019_2020)
    def test_parse_lfp_results_exclude_live_scores(self):

        fpath = os.path.join(os.path.dirname(__file__), 'lfp_2019-2020_24_live.html')
        html = open(fpath, 'r').read()
        results = parse_results_page(html)

        self.assertNotEqual(results, None)
        self.assertEqual(len(results), 1)

        self.assertTrue({'team_a': 'Angers', 'team_b': 'Lille', 'score_a': 0, 'score_b': 2} in results)

    @mock.patch.dict('external.lfp_results.LFP_TEAM_MAP', TEST_LFP_TEAM_MAP_2019_2020)
    def test_parse_lfp_results_exclude_upcoming_matches(self):

        fpath = os.path.join(os.path.dirname(__file__), 'lfp_2019-2020_24.html')
        html = open(fpath, 'r').read()
        results = parse_results_page(html)

        self.assertNotEqual(results, None)
        self.assertEqual(len(results), 1)

        self.assertTrue({'team_a': 'Angers', 'team_b': 'Lille', 'score_a': 0, 'score_b': 2} in results)
