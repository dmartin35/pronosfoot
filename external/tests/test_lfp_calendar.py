import unittest
from external.lfp_calendar import extract_week, extract_teams


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


class TestExtractTeamsFromICal(unittest.TestCase):

    def parse_default(self):

        title = 'ANGERS SCO-FC GIRONDINS DE BORDEAUX'
        team_a, team_b = extract_teams(title)
        self.assertEqual(team_a, 'ANGERS SCO')
        self.assertEqual(team_b, 'FC GIRONDINS DE BORDEAUX')

    def test_parse_multiple_dashes(self):

        title = 'DIJON FCO-AS SAINT-ÉTIENNE'
        team_a, team_b = extract_teams(title)
        self.assertEqual(team_a, 'DIJON FCO')
        self.assertEqual(team_b, 'AS SAINT-ÉTIENNE')

        title = 'AS SAINT-ÉTIENNE-PARIS SAINT-GERMAIN'
        team_a, team_b = extract_teams(title)
        self.assertEqual(team_a, 'AS SAINT-ÉTIENNE')
        self.assertEqual(team_b, 'PARIS SAINT-GERMAIN')
