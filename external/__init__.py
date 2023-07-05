"""
automatically loads the LFP teams map from file 
"""
from collections import OrderedDict
import os
from tools.file import read_file_lines

LFP_TEAM_MAP = OrderedDict()
LFP_TEAM_REVERSE_MAP = {}

LFP_SEASON_ID = '2023-2024'

CALENDAR_URL = 'https://www.ligue1.fr/api/sitecore/MatchIcs/Download'
#SCORE_URL = 'http://www.lfp.fr/ligue1/calendrier_resultat#sai=%d&jour=%s'
#SCORE_URL = 'http://www.lfp.fr/ligue1/competitionPluginCalendrierResultat/changeCalendrierJournee?sai=%d&jour=%s'
#SCORE_URL = 'http://www.lfp.fr/ligue1/calendrier_resultat#sai=%d&jour=%s'
#SCORE_URL = 'http://www.lfp.fr/ligue1/competitionPluginCalendrierResultat/changeCalendrierJournee?sai=%d&jour=%s'
SCORE_URL = 'https://www.ligue1.fr/calendrier-resultats?seasonId=%s&matchDay=%s'

def init_team_map():
    try:
        dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir,'lfp_teams.txt')
        teams_list = read_file_lines(path)
        teams = [team.strip().split(':') for team in teams_list]
        teams = sorted(teams, key=lambda t: t[1])
        for (long_name, short_name) in teams:
            LFP_TEAM_MAP[long_name] = short_name 
            LFP_TEAM_REVERSE_MAP[short_name] = long_name
    except:
        pass

#initializes the global dict for team names
init_team_map()
