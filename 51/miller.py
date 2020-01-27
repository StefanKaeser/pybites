from datetime import datetime, timedelta

# https://pythonclock.org/
PY2_DEATH_DT = datetime(year=2020, month=1, day=1)
BITE_CREATED_DT = datetime.strptime('2018-02-26 23:24:04', '%Y-%m-%d %H:%M:%S')


def py2_earth_hours_left(start_date=BITE_CREATED_DT):
    """Return how many hours, rounded to 2 decimals, Python 2 has
       left on Planet Earth (calculated from start_date)"""
    time_left = PY2_DEATH_DT - start_date
    one_hour = timedelta(hours=1) 
    return round(time_left / one_hour, 2)


def py2_miller_min_left(start_date=BITE_CREATED_DT):
    """Return how many minutes, rounded to 2 decimals, Python 2 has
       left on Planet Miller (calculated from start_date)"""
    time_left = PY2_DEATH_DT - start_date
    earth_year = timedelta(days=365)
    miller_hour = 7 * earth_year 
    miller_minute = miller_hour / 60
    return round(time_left / miller_minute, 2)

