import unittest

import logging
logging.basicConfig()

from external.lfp_results import parse_results_page
from external.lfp_api import get_score

#html = open('lfp_84_01.html', 'r').read()
#res = parse_results_page(html)
#print(res)
# Test: OK


class TestLFPApi(unittest.TestCase):

    def test_get_scores(self):

        self.assertEqual(get_score(1, 'Bastia', 'Paris'), (0, 1))
        self.assertEqual(get_score(1, 'Monaco', 'Guimgamp'), (2, 2))
        self.assertEqual(get_score(1, 'Montpellier', 'Angers'), (1, 0))

