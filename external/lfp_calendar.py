"""
LFP calendar core
"""
import re
from . import LFP_TEAM_MAP

from tools.regexp import extract_regexp_groups
from tools.timezone import convert_utctime_to_timezone

__all__ = ['ical_to_fixtures']

def change_dt_utc_to_local(dt):
    """
    change UTC date time to local time zone Europe/Paris
    """
    return convert_utctime_to_timezone(dt,'%Y%m%dT%H%M%SZ','Europe/Paris','%Y%m%dT%H%M%S')
    
def extract_dt(dt):
    """
    convert date_time format YYYYMMDDTHHMMSSZ as a date YYYY-MM-DD and a time HH:MM:SS
    
    if not possible returns (None, None)
    """
    groups = extract_regexp_groups('(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})T(?P<hour>\d{2})(?P<min>\d{2})(?P<sec>\d{2})',dt)
    date = '%s-%s-%s' % (groups['year'], groups['month'], groups['day'])
    time = '%s:%s:%s' % (groups['hour'], groups['min'], groups['sec'])
    return (date, time)

def extract_teams(summary):
    """
    split the summary to get team names: 
    teamA - team B
    
    return team names if found, (None, None) otherwise
    """
    groups = extract_regexp_groups('(?P<team_a>.*)\s-\s(?P<team_b>.*)',summary)
    return (groups['team_a'],groups['team_b'])

def extract_week(desc):
    """
    get the week from the fixture description: 
    Ligue 1 - XXeme journee
    """
    groups = extract_regexp_groups('Ligue 1 - (?P<week>\d*)\w*',desc)
    return groups['week']

def ical_to_fixtures(ical):
    """
    convert a calendar into a list of fixtures (dict)
    """
    fixtures = []

    for found in re.finditer('BEGIN:VEVENT(?P<event>.*?)END:VEVENT', ical, re.MULTILINE|re.DOTALL):
        event = found.group('event')
        
        dtstart = re.search('^DTSTART:(.*?)$',event,re.MULTILINE|re.DOTALL).group(1)
        summary = re.search('^SUMMARY:(.*?)$',event,re.MULTILINE|re.DOTALL).group(1)
        desc = re.search('^DESCRIPTION:(.*?)$',event,re.MULTILINE|re.DOTALL).group(1)
    
        (date, time) = extract_dt(change_dt_utc_to_local(dtstart))
        (team_a, team_b) = extract_teams(summary)
        week = extract_week(desc)
        
        fixture = {'date': date,
                   'time': time,
                   'team_a': LFP_TEAM_MAP[team_a],
                   'team_b': LFP_TEAM_MAP[team_b],
                   'week': week,
                   }
        
        fixtures.append(fixture)
    
    return fixtures