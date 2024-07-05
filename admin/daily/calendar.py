"""
- get calendar from LFP
- check fixtures date & time
- if fixture postponed, change date&time in fixtures DB
"""
from django.conf import settings

from tools.log import _log
from external.ligue1.api import get_calendar
from season.models import Team
from season.models import Fixture
from tools.dtconvert import str_to_date
from tools.dtconvert import str_to_time

def check_calendar():
    """
    get calendar from LFP and check fixtures date&time
    if any change, set new date&time and log it
    """
    lfp_cal = get_calendar()
    allow_schedule_backward = len(lfp_cal) == 380
    for fixt_dict in lfp_cal:
        #locally store fixture info
        team_a = Team.objects.get(name=fixt_dict['team_a'])
        team_b = Team.objects.get(name=fixt_dict['team_b'])
        day = str_to_date(fixt_dict['date'], settings.DATE_FORMAT)
        hour = str_to_time(fixt_dict['time'], settings.TIME_FORMAT)

        #get fixture from DB - should get only one entry
        fixture = Fixture.objects.get(team_a=team_a, team_b=team_b)

        #check date/time, modify if needed and log change
        if fixture:

            # do not change a date for a match that has a final score
            if fixture.score_a is not None or fixture.score_b is not None:
                continue

            old_day = fixture.day
            old_time = fixture.hour

            # change only for either day/date in the future or different scheduled time for the same day
            # we don't want to update with a date in the past
            # (when duplicated matches in wrong order in ICal for postponed matches)
            # case 1: always update for a more recent day ie postponed/re-scheduled matches
            # case 2: same day but scheduled time has changed
            # case 3: was not scheduled, but possibly day(s) before
            # case 4: game is reschedule before initial date in replacement of another TV game that is postponed
            # (only when no duplicates!)
            if day > old_day \
                    or (day == old_day and old_time != hour) \
                    or (day != old_day and str(old_time) == '00:00:00') \
                    or (day < old_day and allow_schedule_backward):
                log_str = '%s (%s) %s-%s %s %s'% (fixture.id, fixture.week,
                    fixture.team_a, fixture.team_b, fixture.day, fixture.hour)

                #save date&time change in DB
                fixture.day = day
                fixture.hour = hour
                fixture.save()

                #log change
                _log('%s -> %s %s'%(log_str,day,hour))
