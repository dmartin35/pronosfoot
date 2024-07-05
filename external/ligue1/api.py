from __future__ import annotations  # allow typing syntax for Python 3.10+
from  typing import Any
import requests
from memoize import memoize

from . import L1_CHAMPIONSHIP_ID, L1_CHAMPIONSHIP_SEASON
from .calendar_utils import parse_dt, change_dt_utc_to_local, extract_dt

__all__ = ['get_teams', 'get_calendar', 'get_score']


L1_CHAMPIONSHIP_SETTINGS = "https://ma-api.ligue1.fr/championships-settings"
L1_CHAMPIONSHIP_CALENDAR = "https://ma-api.ligue1.fr/championship-calendar/%s"
L1_CHAMPIONSHIP_MATCHES = "https://ma-api.ligue1.fr/championship-matches/championship/%s/game-week/%s?season=%s"


@memoize(timeout=3600)
def get_teams():
    """
    returns the list of teams for the season,
    from L1 first week matches list
    """
    r = requests.get(L1_CHAMPIONSHIP_MATCHES % (L1_CHAMPIONSHIP_ID, 1, L1_CHAMPIONSHIP_SEASON))
    matches = r.json().get('matches', [])

    teams = []
    teams.extend([m["home"]["clubIdentity"]["officialName"] for m in matches])
    teams.extend([m["away"]["clubIdentity"]["officialName"] for m in matches])
    teams = sorted(teams)

    return teams


@memoize(timeout=3600)
def get_calendar():
    """
    L1 API calendar endpoint return only the weeks start/end dates
    alongside matches identifiers, but not team names not game date

    we'll go across every week to get all matches with all info

    @return: the full calendar of the current season
    @return: list of fixture dict if available, empty list otherwise
    dict contains following keys: week, date, time, team_a, team_b
    """
    # fetch championship settings to obtain the number of weeks in a season
    r = requests.get(L1_CHAMPIONSHIP_SETTINGS)
    champ_settings = r.json()["championships"].get(L1_CHAMPIONSHIP_ID, {})
    if not champ_settings:
        return []

    # iterate over every week, to obtain all matches ie full calendar
    fixtures = []
    for week in range(1, champ_settings["gameWeeks"] + 1):
        r = requests.get(L1_CHAMPIONSHIP_MATCHES % (L1_CHAMPIONSHIP_ID, week, L1_CHAMPIONSHIP_SEASON))
        matches = r.json().get('matches', [])

        for match in matches:
            team_home = match["home"]["clubIdentity"]["officialName"]
            team_away = match["away"]["clubIdentity"]["officialName"]
            match_date, match_hour = extract_dt(change_dt_utc_to_local(parse_dt(match["date"])))
            fixtures.append(
                {
                    'date': match_date,
                    'time': match_hour,
                    'team_a': team_home,
                    'team_b': team_away,
                    'week': week,
                }
            )

    return fixtures


@memoize(timeout=60)
def _get_matches(week: int) -> Any:
    """
    we cache the query not to trigger an api call when iterating over all games of a given week,
    as we iterate of fixtures results from external caller - but not on the returned matches list -
    :param week:
    :return:
    """
    print(">> get matches ", week)
    r = requests.get(L1_CHAMPIONSHIP_MATCHES % (L1_CHAMPIONSHIP_ID, week, L1_CHAMPIONSHIP_SEASON))
    r.raise_for_status()

    return r.json().get('matches', [])


def get_score(week: int, team_a: str, team_b: str) -> (int | None, int | None):
    """
    returns a match score from the LFP site

    @param week: week of the match
    @param team_a: home team of the match
    @param team_b: away team of the match

    @return the score of the match
    @return tuple (score_a, score_b) if found, (None,None) otherwise
    """
    print(">> get score", week, team_a, team_b)
    matches = _get_matches(week)


    for match in matches:
        team_home = match["home"]["clubIdentity"]["officialName"]
        team_away = match["away"]["clubIdentity"]["officialName"]
        # period = match['period']
        is_live = match['isLive']

        if team_home == team_a and team_away == team_b and not is_live:  # @todo check period is enf of game
            score_home = match["home"].get("score")
            score_away = match["away"].get("score")

            return score_home, score_away

    return None, None


#print(get_teams())
#print(get_calendar())
print(get_score(1, "Angers", "Lens"))
