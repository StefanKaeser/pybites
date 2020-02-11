from datetime import date

NUMBER_MAY = 5
NUMBER_SUNDAY = 7

#def get_mothers_day_date(year):
#    """Given the passed in year int, return the date Mother's Day
#       is celebrated assuming it's the 2nd Sunday of May."""
#    first_found = False
#    for day in range(1, 15):
#        d = date(year=year, month=NUMBER_MAY, day=day)
#        _, _, weekday = d.isocalendar()
#        if weekday == NUMBER_SUNDAY:
#            if first_found:
#                return d
#            first_found = True

#def get_mothers_day_date(year):
#    """Given the passed in year int, return the date Mother's Day
#       is celebrated assuming it's the 2nd Sunday of May."""
#    dates = [date(year=year, month=NUMBER_MAY, day=day) for day in range(1, 15)]
#    sundays = [d for d in dates if d.isocalendar()[2] == NUMBER_SUNDAY]
#    return sundays[1]

from dateutil.relativedelta import relativedelta, SU

def get_mothers_day_date(year):
    """Given the passed in year int, return the date Mother's Day
       is celebrated assuming it's the 2nd Sunday of May."""
    first_of_may = date(year=year, month=NUMBER_MAY, day=1)
    return first_of_may + relativedelta(weekday=SU(2))
