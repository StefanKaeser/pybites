from collections import defaultdict
import os
from urllib.request import urlretrieve

from bs4 import BeautifulSoup


# prep data
# tmp = os.getenv("TMP", "/tmp")
tmp = os.path.curdir
page = "us_holidays.html"
holidays_page = os.path.join(tmp, page)
urlretrieve(f"https://bites-data.s3.us-east-2.amazonaws.com/{page}", holidays_page)

with open(holidays_page) as f:
    content = f.read()


def get_us_bank_holidays(content=content):
    """Receive scraped html output, make a BS object, parse the bank
       holiday table (css class = list-table), and return a dict of
       keys -> months and values -> list of bank holidays"""
    soup = BeautifulSoup(content, "html.parser")
    holiday_table = soup.find("table", {"class": "list-table"})

    months = [tag.string.split("-")[1] for tag in holiday_table.find_all("time")]
    holiday_names = [tag.string.strip() for tag in holiday_table.find_all("a")]

    holidays = defaultdict(list)
    for month, name in zip(months, holiday_names):
        holidays[month].append(name)

    return holidays
