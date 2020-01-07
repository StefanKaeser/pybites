from datetime import datetime, timedelta, date

TODAY = date(2018, 11, 12)


def extract_dates(data):
    """Extract unique dates from DB table representation as shown in Bite"""
    data = data.strip()
    lines = data.splitlines()[3:-1]
    date_strings = [line.split("|")[1].strip() for line in lines]
    dates = [datetime.strptime(string, "%Y-%m-%d").date() for string in date_strings]
    return set(dates)


def calculate_streak(dates):
    """Receives sequence (set) of dates and returns number of days
       on coding streak.

       Note that a coding streak is defined as consecutive days coded
       since yesterday, because today is not over yet, however if today
       was coded, it counts too of course.

       So as today is 12th of Nov, having dates 11th/10th/9th of Nov in
       the table makes for a 3 days coding streak.

       See the tests for more examples that will be used to pass your code.
    """
    dates = [TODAY] + sorted(dates, reverse=True)

    streak = 0
    for date1, date2 in zip(dates, dates[1:]):
        diff = date1 - date2
        if diff <= timedelta(days=1):
            streak += 1
        else:
            break
    return streak
