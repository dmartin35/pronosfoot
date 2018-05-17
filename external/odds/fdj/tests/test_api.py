import unittest
from external.odds.fdj.api import get_odds


@unittest.skip('Skip broken FDJ odds API')
class TestFDJOdds(unittest.TestCase):
    def test_get_odds(self):
        """
        this test ensure the retrieval of FDJ odds is not broken over time
        :return: 
        """
        odds = get_odds()
        self.assertNotEqual(odds, None)
        self.assertNotEqual(odds, {})

        self.assertTrue(len(odds.keys()) > 0)

    def test_print_odds(self):
        """
        Simple test to print out current odds found in the FDj page
        """
        for match, odds in get_odds().items():
            print(match, odds)


if __name__ == "__main__":
    for match, odds in get_odds().items():
        print(match, odds)
