from dateutil.rrule import rrule, DAILY


def get_missing_dates(dates):
    """Receives a range of dates and returns a sequence
       of missing datetime.date objects (no worries about order).

       You can assume that the first and last date of the
       range is always present (assumption made in tests).

       See the Bite description and tests for example outputs.
    """
    dates_sorted = sorted(dates)
    start, end = dates_sorted[0], dates_sorted[-1]

    all_dates = [dt.date() for dt in rrule(DAILY, dtstart=start, until=end)]
    missing_dates = set(all_dates) - set(dates_sorted)

    return missing_dates
