"""
LFP calendar core
"""
import arrow
from ics import Calendar
import logging
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
    dt = arrow.get(dt)
    date = dt.format('YYYY-MM-DD')
    time = dt.format('HH:mm:ss')
    return date, time


def extract_teams(summary):
    """
    split the summary to get team names: 
    teamA - team B
    
    return team names if found, (None, None) otherwise
    """
    if summary.startswith((
        "AS SAINT-ÉTIENNE",
        "PARIS SAINT-GERMAIN"
    )):
        a1, a2, b = summary.split('-', 2)
        return "%s-%s" % (a1, a2), b

    return summary.split('-', 1)


def extract_week(desc):
    """
    get the week from the fixture description: 
    Ligue 1 - XXeme journee
    """
    groups = extract_regexp_groups('Ligue 1 (?P<naming>\w+\s)?- (?P<week>\d*)\w*',desc)
    return groups['week']


def ical_to_fixtures(ical):
    """
    convert a calendar into a list of fixtures (dict)
    """
    fixtures = []

    cal = Calendar(ical)
    for event in cal.events:
        try:
            #date, time = extract_dt(change_dt_utc_to_local(event.begin))
            date, time = extract_dt(event.begin)
            team_a, team_b = extract_teams(event.name)
            try:
                week = extract_week(event.description)
            except:
                week = None

            fixture = {'date': date,
                       'time': time,
                       'team_a': LFP_TEAM_MAP[team_a],
                       'team_b': LFP_TEAM_MAP[team_b],
                       'week': week,
                       }

            fixtures.append(fixture)
        except:
            logging.exception('Error parsing fixture event from ical')

    return fixtures