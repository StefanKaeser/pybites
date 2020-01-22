from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

PYBITES_BORN = datetime(year=2016, month=12, day=19)


def gen_special_pybites_dates():
    special_date = PYBITES_BORN
    next_birthday = PYBITES_BORN + relativedelta(years=1)

    while True:
        special_date += timedelta(days=100)
        if special_date > next_birthday:
            yield next_birthday
            next_birthday += relativedelta(years=1)
        yield special_date
