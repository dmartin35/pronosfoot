import bs4
import requests
from collections import namedtuple
from memoize import memoize
import contextlib
from external.odds.betclic import TEAM_MAP

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BETCLIC_L1_URL = 'https://www.betclic.fr/football-s1/ligue-1-uber-eats-c4'


Odds = namedtuple('Odds', ['win', 'draw','lose'])


def _download_odds():
    """
    Download html from
    :return:
    """
    resp = requests.get(BETCLIC_L1_URL, headers={}, verify=False)
    resp.raise_for_status()
    return resp.content.decode('utf-8')


def _parse_odds(html):
    """
    Parse the odds and returns
    :param html: full html content of the downloaded page - to parse
    :return: list of (teamA, teamB, odds win, odds draw, odds lose)
    """
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # odds = soup.select('div.match-entry')
    odds = soup.find_all('div', class_='cardMatch')

    raw = []
    for odd in odds:
        with contextlib.suppress(Exception):
            teams = odd.select('.betBox_matchName')[0]
            teams = teams.select('.betBox_contestantName')
            teams = [t.string.strip() for t in teams]

            match_odds = odd.select('.betBox_wrapperOdds > app-default-market')[0]
            match_odds = match_odds.select('.betBox_odds .oddValue')
            wdl = [tag.string for tag in match_odds]

            raw.append(tuple(teams + wdl))

    return raw


def _get_odds_raw():
    """
    returns the list of raw odds from FDJ - parions sport page - for Ligue1
    fetches LFP html page then parse it to extract as many odds as possible
    :return: list of (teamA, teamB, odds win, odds draw, odds lose)
    """
    return _parse_odds(_download_odds())


def convert_team_name(name):
    """
    convert external team name into internal team name
    """
    custom = TEAM_MAP.get(name)
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
        team_a = convert_team_name(team_a)
        team_b = convert_team_name(team_b)
        odds[(team_a, team_b)] = Odds(win, draw, lose)

    return odds

