from ics import Calendar, Event
from datetime import timedelta, datetime


def fixtures_to_ical(fixtures) -> str:
    c = Calendar()

    year_start, year_end = fixtures[0].day.year, fixtures[len(fixtures)-1].day.year

    for f in fixtures:
        e = Event()
        e.name = f"{f.team_a} - {f.team_b} (J{f.week}) [football]"
        e.uid = f"LFP_L1_{year_start}_{year_end}_{f.id}"

        dt = f"{f.day}T{f.hour}+02:00"
        e.begin = datetime.fromisoformat(dt)
        e.duration = timedelta(hours=2)
        #e.end = e.begin + timedelta(hours=2)

        c.events.add(e)

    return str(c)
