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
            team_a = result.select('div.club.home a span.calendarTeamNameDesktop')[0].string
            team_b = result.select('div.club.away a span.calendarTeamNameDesktop')[0].string
            team_a = escape_accent(team_a)
            team_b = escape_accent(team_b)

            scores = result.select('div.result a span')
            score_a = int(scores[0].string)
            score_b = int(scores[-1].string)

            results.append({'team_a': LFP_TEAM_MAP[team_a],
                            'team_b': LFP_TEAM_MAP[team_b],
                            'score_a': score_a,
                            'score_b': score_b
                            })

        except Exception:
            logging.exception('unable to fetch match score')

    return results
