from datetime import date

from dateutil.rrule import rrule, DAILY

TODAY = date(year=2018, month=11, day=29)
NUMBER_OF_DAYS = 100


def get_hundred_weekdays(start_date=TODAY):
    """Return a list of hundred date objects starting from
       start_date up till 100 weekdays later, so +100 days
       skipping Saturdays and Sundays"""
    dts = list(
        rrule(DAILY, count=NUMBER_OF_DAYS, byweekday=range(5), dtstart=start_date,)
    )
    dates = [dt.date() for dt in dts]
    return dates
