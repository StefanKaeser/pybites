import pytz

MEETING_HOURS = range(6, 23)  # meet from 6 - 22 max
TIMEZONES = set(pytz.all_timezones)


def within_schedule(utc, *timezones):
    """Receive a utc datetime and one or more timezones and check if
       they are all within schedule (MEETING_HOURS)"""
    utc = pytz.utc.localize(utc)

    for timezone in timezones:
        if timezone not in TIMEZONES:
            raise ValueError

        dt_in_timezone = utc.astimezone(pytz.timezone(timezone))
        if dt_in_timezone.hour not in MEETING_HOURS:
            return False

    return True
