import bs4
import requests
import json
from collections import namedtuple
from memoize import memoize
import contextlib
from external.odds.betclic import TEAM_MAP

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BETCLIC_L1_URL = 'https://www.betclic.fr/football-sfootball/ligue-1-mcdonald-s-c4'

BETCLIC_API_URL = 'https://offer.cdn.betclic.fr/api/pub/v2/competitions/4?application=2&countrycode=fr&fetchMultipleDefaultMarkets=true&language=fr&sitecode=frfr'


Odds = namedtuple('Odds', ['win', 'draw','lose'])


def _download_odds(url=BETCLIC_L1_URL):
    """
    Download html from
    :return:
    """
    resp = requests.get(url, headers={}, verify=False)
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
    odds = soup.find_all('a', class_='cardEvent')

    raw = []
    for odd in odds:
        with contextlib.suppress(Exception):
            teams = odd.select('.scoreboard_wrapper')[0]
            teams = teams.select('.scoreboard_contestantLabel')

            teams = [t.string.strip() for t in teams]

            match_odds = odd.select('.market_odds')[0]
            match_odds = match_odds.select('.btn.is-odd')
            wdl = [btn_odd.select(".btn_label")[1].text.strip() for btn_odd in match_odds]

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


def get_odds_from_html():
    """
    formats the raw structure into dict with team name matching internal names
    :return: dict of (teamA, teamB):  Odds(win, draw, lose)
    """
    raw = _get_odds_raw()
    odds = {}

    for line in raw:
        try:
            team_a, team_b, win, draw, lose = line
            team_a = convert_team_name(team_a)
            team_b = convert_team_name(team_b)
            odds[(team_a, team_b)] = Odds(win, draw, lose)
        except ValueError:
            pass  # ignore in case of unpacking with value error for some lines

    return odds


def get_odds_from_api():
    """
    formats the raw structure into dict with team name matching internal names
    :return: dict of (teamA, teamB):  Odds(win, draw, lose)
    """
    odds = {}

    raw = _download_odds(url=BETCLIC_API_URL)
    with contextlib.suppress(Exception):
        data = json.loads(raw)

        events = data.get("unifiedEvents") or []
        for evt in events:
            try:
                teams = evt.get("name", "")
                if not teams:
                    continue

                team_a, team_b = teams.split(' - ')
                team_a = convert_team_name(team_a)
                team_b = convert_team_name(team_b)

                markets = evt.get("markets") or []
                if not len(markets) >= 1:
                    continue

                mkt = markets[0]
                wdl = mkt.get("selections") or []

                if not len(wdl) >= 3:
                    continue

                win = wdl[0].get("odds")
                draw = wdl[1].get("odds")
                lose = wdl[2].get("odds")

                odds[(team_a, team_b)] = Odds(win, draw, lose)


            except Exception:
                pass # if one event is failing, we do not break all of them


    return odds


@memoize(timeout=300)
def get_odds():
    return get_odds_from_html()