"""
TIMEZONE TOOLS
"""
import pytz
import datetime

def convert_utctime_to_timezone(utctime,utcformat,zone, zoneformat):
    """
    convert a UTC date/time (in a specified format) to a local time zone (in a specified format)
   
    @param utctime: UTC time to convert
    @param utcformat: iso string format of the UTC time
    @param zone: the zone to convert the UTC time to
    @param zoneformat: iso string format of the converted UTC time
    """
    #create the final time zone
    finaltz = pytz.timezone(zone)
    #create datetime obj from iso string
    dt = datetime.datetime.strptime(utctime,utcformat)
    #need to set first to UTC then to change to given time zone, to handle Daylight Saving Time

    dtime = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=pytz.utc).astimezone(finaltz)
    #create back iso date time string
    return dtime.strftime(zoneformat)

if __name__ == '__main__':
    print(convert_utctime_to_timezone('20110801T183000Z','%Y%m%dT%H%M%SZ','Europe/Paris','%Y%m%dT%H%M%S%z'))