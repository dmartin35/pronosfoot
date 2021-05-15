import os
import unittest
from unittest import mock
from external.odds.betclic.api import get_odds, get_odds_from_html
from memoize import delete_memoized



BETCLIC_TESTS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class TestBetclicOdds(unittest.TestCase):
    def setUp(self):
        """
        Clears odds memoize cache - to ensure not to get cached result from a previous unit test
        """
        delete_memoized(get_odds)

    #@unittest.skip('This test is disabled for production due to daily page changes which leads to no odds some days')
    def test_get_odds(self):
        """
        this test ensure the retrieval of betclic odds is not broken over time
        """
        odds = get_odds()
        self.assertNotEqual(odds, None)
        self.assertNotEqual(odds, {})
        self.assertTrue(len(odds.keys()) > 0)

    def test_print_odds(self):
        """
        Simple test to print out current odds found in the betclic page
        """
        for match, odds in get_odds().items():
            print(match, odds)


class TestLocalBetclicOdds(unittest.TestCase):

    def setUp(self):
        """
        * Uses local html page for odds - downloaded once from the web site
        * Clears odds memoize cache - to ensure not to get cached result from a previous unit test
        """
        with open(os.path.join(BETCLIC_TESTS_FOLDER, 'betclic-ligue1.html'), 'r') as f:
            self.html = f.read()

        delete_memoized(get_odds)

    def test_parse_odds(self):
        """
        Parse local betclic page to get odds
        """
        with mock.patch('external.odds.betclic.api._download_odds', return_value=self.html):
            odds = get_odds_from_html()
            self.assertNotEqual(odds, None)
            self.assertNotEqual(odds, {})
            self.assertTrue(len(odds.keys()) > 0)

    def test_print_odds(self):
        """
        Parse & prints odds without downloading from betclic website,
        but using local html file
        """
        with mock.patch('external.odds.betclic.api._download_odds', return_value=self.html):
            for match, odds in get_odds_from_html().items():
                print(match, odds)


if __name__ == "__main__":
    for match, odds in get_odds().items():
        print(match, odds)
