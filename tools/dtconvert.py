"""
Date & Time Convertion Module
"""
import datetime

def str_to_date(date_str,format):
    """
    convert a date string, in a given format, to a date obj
    """
    d = datetime.datetime.strptime(date_str,format)
    return datetime.date(d.year,d.month,d.day)

def str_to_time(time_str,format):
    """
    convert a time string, in a given format, to a time obj
    """
    t = datetime.datetime.strptime(time_str,format)
    return datetime.time(t.hour,t.minute,t.second)

if __name__ == '__main__':
    a = datetime.date(2011,8,6)
    b = str_to_date('2011-08-06','%Y-%m-%d')
    print(a == b)
    
    c = datetime.time(21,30,0o2)
    d = str_to_time('21:30:02','%H:%M:%S')
    print(c == d)
