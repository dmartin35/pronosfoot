import unittest
from external.lfp_calendar import extract_week


class TestExtractWeekFromICal(unittest.TestCase):

    def test_week_from_desc(self):
        desc = 'Ligue 1 - 3ème journée'
        week = extract_week(desc)
        self.assertEqual(week, '3')

    def test_week_from_desc_with_naming(self):
        desc = 'Ligue 1 Conforama - 13ème journée - En direct sur beIN SPORTS 1'
        week = extract_week(desc)
        self.assertEqual(week, '13')

    def test_parse_ical_accented_chars(self):
        """ Test ical parsing with teams with accented characters (é/î/...)"""
        pass
