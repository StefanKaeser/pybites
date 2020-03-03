import csv

import requests
from collections import Counter

CSV_URL = "https://bites-data.s3.us-east-2.amazonaws.com/community.csv"


def get_csv():
    """Use requests to download the csv and return the
       decoded content"""
    with requests.get(CSV_URL) as r:
        content = (line.decode("utf-8") for line in r.iter_lines())
    return content


def create_user_bar_chart(content):
    """Receives csv file (decoded) content and print a table of timezones
       and their corresponding member counts in pluses to standard output
    """
    reader = csv.DictReader(content)
    timezones = [row["tz"] for row in reader]
    tz_ctr = Counter(timezones)
    string = ""
    for tz, num_members in tz_ctr.items():
        string += f"{tz:<21}| {'+'*num_members}\n"
    print(string)
