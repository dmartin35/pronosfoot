import arrow


def parse_dt(dt: str) -> arrow.Arrow:
    """
    parse a date_time string as ISO8601 format into date/time representation object
    """
    return arrow.get(dt)


def change_dt_utc_to_local(dt: arrow.Arrow) -> arrow.Arrow:
    """
    change UTC date time to local time zone Europe/Paris
    """
    return dt.to('Europe/Paris')


def extract_dt(dt: arrow.Arrow) -> arrow.Arrow:
    """
    extract date_time as string format ISO8601 YYYYMMDDTHHMMSSZ as a date YYYYÒ-MM-DD and a time HH:MM:SS

    if not possible returns (None, None)
    """
    date = dt.format('YYYY-MM-DD')
    time = dt.format('HH:mm:ss')
    return date, time


