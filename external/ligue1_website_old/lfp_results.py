"""
LFP results page parser
"""
import bs4
import re
import logging
from . import LFP_TEAM_MAP
from tools.escape import escape_accent


def parse_results_page(content):
    """
    parse the entire html page content, 
    to extract list of fixtures that have a match score
    """
    soup = bs4.BeautifulSoup(content, 'html.parser')

    match_results = soup.select('ul li.match-result')

    results = []
    for result in match_results:

        try:
            # skip live matches
            if 'live' in result.attrs.get('class', []):
                continue

            team_a = result.select('div.club.home span.calendarTeamNameDesktop')[0].string
            team_b = result.select('div.club.away span.calendarTeamNameDesktop')[0].string
            team_a = escape_accent(team_a)
            team_b = escape_accent(team_b)

            scores = result.select('div.result span span')
            score_a = scores[0].string
            score_b = scores[-1].string

            # skip matches without score - not started yet
            if not score_a or not score_b:
                continue

            results.append({'team_a': LFP_TEAM_MAP[team_a],
                            'team_b': LFP_TEAM_MAP[team_b],
                            'score_a': int(score_a),
                            'score_b': int(score_b)
                            })

        except Exception:
            logging.exception('unable to fetch match score')

    return results
