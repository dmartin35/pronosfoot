import bs4
import re
import requests
from collections import namedtuple
from memoize import memoize

from external.odds.fdj import FDJ_TEAM_MAP


PARIONS_SPORT_URL = 'https://www.enligne.parionssport.fdj.fr/paris-football/france/ligue-1'
ODD_REGEX = re.compile('.*?<li class="outcomes.*?<a.*?title="(?P<match>.*?)".*?<span class="formatted_price">(?P<win>.*?)</span>.*?<span class="formatted_price">(?P<draw>.*?)</span>.*?<span class="formatted_price">(?P<lose>.*?)</span>.*?', re.MULTILINE | re.DOTALL | re.IGNORECASE)

Odds = namedtuple('Odds', ['win', 'draw','lose'])


def _get_odds_raw():
    """
    returns the list of raw odds from FDJ - parions sport page - for Ligue1
    getches LFP html page then parse it to extract as many odds as possible
    :return: list of (teamA, teamB, odds win, odds draw, odds lose)
    """
    resp = requests.get(PARIONS_SPORT_URL, headers={})
    resp.raise_for_status()
    content = resp.content.decode('utf-8')

    soup = bs4.BeautifulSoup(content, 'html.parser')
    odds = soup.select('#tab_gameevent ul.market')

    raw = []
    for odd in odds:
        match = re.match(ODD_REGEX, str(odd))
        teams, win, draw, lose = match.group('match'), match.group('win'), match.group('draw'), match.group('lose')
        teams, win, draw, lose = teams.strip().split(' - '), win.strip(), draw.strip(), lose.strip()

        raw.append(tuple(teams) + (win, draw, lose))
    return raw


def convert_fdj_team_name(name):
    """
    convert FDJ team name into internal team name
    """
    custom = FDJ_TEAM_MAP.get(name)
    return custom if custom else name.title()


@memoize(timeout=300)
def get_odds():
    """
    formats the raw structure into dict with team name matching internal names
    :return: dict of (teamA, teamB):  Odds(win, draw, lose)
    """
    raw = _get_odds_raw()
    odds = {}

    for line in raw:
        team_a, team_b, win, draw, lose = line
        team_a = convert_fdj_team_name(team_a)
        team_b = convert_fdj_team_name(team_b)
        odds[(team_a, team_b)] = Odds(win, draw, lose)

    return odds

