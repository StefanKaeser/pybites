from datetime import datetime, timedelta
import re

NOW = datetime(year=2019, month=2, day=6, hour=22, minute=0, second=0)


UNI_PATTERNS = {
    "days": [r"\d+d",],
    "hours": [r"\d+h",],
    "minutes": [r"\d+m",],
    "seconds": [r"\d+s", r"\d+$"],
}


def add_todo(delay_time: str, task: str, start_time: datetime = NOW) -> str:
    """
    Add a todo list item in the future with a delay time.

    Parse out the time unit from the passed in delay_time str:
    - 30d = 30 days
    - 1h 10m = 1 hour and 10 min
    - 5m 3s = 5 min and 3 seconds
    - 45 or 45s = 45 seconds

    Return the task and planned time which is calculated from
    provided start_time (here default = NOW):
    >>> add_todo("1h 10m", "Wash my car")
    >>> "Wash my car @ 2019-02-06 23:10:00"
    """
    unit_value = dict()
    for unit, patterns in UNI_PATTERNS.items():
        matches = [re.search(pattern, delay_time) for pattern in patterns]
        matches = [match for match in matches if match is not None]

        if len(matches) == 0:
            continue
        elif len(matches) > 1:
            raise ValueError(
                f"Your delay time {delay_time} gives the {unit} unit"
                " in multiple formats."
            )
        else:
            value = int(re.search(r"\d+", matches[0].group()).group())
            unit_value[unit] = value

    td = timedelta(**unit_value)
    task_dt = start_time + td
    return f"{task} @ {task_dt}"
