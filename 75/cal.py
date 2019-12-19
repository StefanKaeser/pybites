def get_weekdays(calendar_output):
    """Receives a multiline Unix cal output and returns a mapping (dict) where
       keys are int days and values are the 2 letter weekdays (Su Mo Tu ...)"""
    day_weekday = dict()

    _, weekdays, *day_lines, _ = [
        line.strip().split() for line in calendar_output.split("\n")
    ]
    day_lines = [[int(day) for day in days] for days in day_lines]

    for days in day_lines:
        if days[0] == 1:
            days = list(zip(days[::-1], weekdays[::-1]))
        else:
            days = list(zip(days, weekdays))

        day_weekday.update(days)

    return day_weekday
