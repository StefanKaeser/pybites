from collections import namedtuple
from datetime import datetime

TimeOffset = namedtuple("TimeOffset", "offset date_str divider")

NOW = datetime.now()
MINUTE, HOUR, DAY = 60, 60 * 60, 24 * 60 * 60
TIME_OFFSETS = (
    TimeOffset(10, "just now", None),
    TimeOffset(MINUTE, "{} seconds ago", None),
    TimeOffset(2 * MINUTE, "a minute ago", None),
    TimeOffset(HOUR, "{} minutes ago", MINUTE),
    TimeOffset(2 * HOUR, "an hour ago", None),
    TimeOffset(DAY, "{} hours ago", HOUR),
    TimeOffset(2 * DAY, "yesterday", None),
)


def pretty_date(date):
    """Receives a datetime object and converts/returns a readable string
       using TIME_OFFSETS"""
    if not isinstance(date, datetime):
        raise ValueError("Input has to be a datetime object.")

    td = NOW - date
    seconds = int(td.total_seconds())
    if seconds < 0:
        raise ValueError("Does not support dates in the future.")

    for offset, date_str, divider in TIME_OFFSETS:
        if seconds < offset:
            seconds = int(seconds / divider) if divider else seconds
            return date_str.format(seconds)
    # Dates beyond 2 days
    return date.strftime("%m/%d/%y")
