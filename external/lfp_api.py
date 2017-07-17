"""
LFP API
"""
from . import LFP_TEAM_MAP
from . import LFP_SEASON_ID
from . import SCORE_URL
from . import CALENDAR_URL

from tools.web import get_url_content
from tools.escape import escape_accent
from .lfp_calendar import ical_to_fixtures
from .lfp_results import parse_results_page

__all__ = ['get_teams','get_score','get_calendar']

def get_teams():
    """
    returns the list of teams
    """
    return list(LFP_TEAM_MAP.values())

def get_calendar():
    """
    @return: the full calendar of the current season
    @return: list of fixture dict if available, empty list otherwise
    dict contains following keys: week, date, time, team_a, team_b  
    """
    try:
        ical = get_url_content(CALENDAR_URL)
        # ical = ical.encode('utf-8')
        ical = escape_accent(ical)
        return ical_to_fixtures(ical)
    except Exception as e:
        print('error getting LFP calendar:',e)
        pass
    return []

def get_score(week, team_a, team_b):
    """
    returns a match score from the LFP site
    
    @param week: week of the match
    @param team_a: home team of the match
    @param team_b: away team of the match
    
    @return the score of the match 
    @return tuple (score_a, score_b) if found, (None,None) otherwise
    """
    try:
        pagecontent = get_url_content(SCORE_URL%(LFP_SEASON_ID,week))
        #pagecontent = pagecontent.encode('utf-8')
        results = parse_results_page(pagecontent)
        for result in results:
            if result['team_a'] == team_a and result['team_b']:
                return (result['score_a'],result['score_b'])
    except Exception as err:
        print('error getting match score:', err)
        pass
    return (None,None)
