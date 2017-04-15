"""
LFP results page parser
"""
import re
import logging
from . import LFP_TEAM_MAP
from tools.escape import escape_accent

#this regexp extract all fixtures that have a score
FIXTURES_SCORES_REGEXP = '<tr.*?>.*?<td.*?/td>\s*<td.*?<a.*?>(?P<team_a>.*?)</a>.*?</td>\s*<td.*?/td>\s*<td.*?<a.*?>(?:(?P<score_a>\d+?)\s*-\s*(?P<score_b>\d+?)|(?:<.*?>))</a>.*?</td>\s*<td.*?/td>\s*<td.*?<a.*?>(?P<team_b>.*?)</a>.*?</td>.*?</tr>.*?'

def parse_results_page(content):
    """
    parse the entire html page content, 
    to extract list of fixtures that have a match score
    """
    results = []
    for match in re.finditer(FIXTURES_SCORES_REGEXP, content, re.MULTILINE | re.DOTALL):
        try:
            team_a = escape_accent(match.group('team_a').strip())
            team_b = escape_accent(match.group('team_b').strip())
            score_a = int(match.group('score_a')) if match.group('score_a') else None
            score_b = int(match.group('score_b')) if match.group('score_b') else None
            results.append({'team_a':LFP_TEAM_MAP[team_a],
                            'team_b':LFP_TEAM_MAP[team_b],
                            'score_a':score_a,
                            'score_b':score_b
                            })
        except Exception as err:
            logging.error('unable to fetch match score: {}'.format(err))
    return results
