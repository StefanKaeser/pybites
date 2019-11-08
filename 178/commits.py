from collections import Counter
import os
from urllib.request import urlretrieve

from dateutil.parser import parse

commits = os.path.join('./', 'commits.txt')
urlretrieve('https://bit.ly/2H1EuZQ', commits)

# you can use this constant as key to the yyyymm:count dict
YEAR_MONTH = '{y}-{m:02d}'

def get_min_max_amount_of_commits(commit_log: str = commits,
                                  year: int = None) -> (str, str):
    """
    Calculate the amount of inserts / deletes per month from the
    provided commit log.

    Takes optional year arg, if provided only look at lines for
    that year, if not, use the entire file.

    Returns a tuple of (least_active_month, most_active_month)
    """
    yearmonth_numchanges = Counter()
    with open(commits) as R:
        for line in R.readlines():
            line = line.lstrip("Date:")
            date, changes = line.split("|")

            date = parse(timestr=date)
            if year and date.year != year:
                continue
            date = date.strftime("%Y-%m")

            changes = [int(word) for word in changes.split(" ")
                                                    if word.isdigit()]
            # Only count insertes and deletes as a change
            numchanges = sum(changes[1:])

            yearmonth_numchanges[date] += numchanges
    
    min_numchanges = yearmonth_numchanges.most_common()[-1][0] 
    max_numchanges = yearmonth_numchanges.most_common(1)[0][0] 
    
    return min_numchanges, max_numchanges

print(get_min_max_amount_of_commits())
