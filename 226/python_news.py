from collections import namedtuple
import re
import operator

from bs4 import BeautifulSoup
import requests

# feed = https://news.python.sc/, to get predictable results we cached
# first two pages - use these:
# https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index.html
# https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index2.html

Entry = namedtuple("Entry", "title points comments")


def get_top_titles(url, top=5):
    """Parse the titles (class 'title') using the soup object.
       Return a list of top (default = 5) titles ordered descending
       by number of points and comments.
    """
    soup = _create_soup_obj(url)
    title_tags = _get_title_tags(soup)

    entries = []
    for title_tag in title_tags:
        entry = _create_entry(title_tag)
        entries.append(entry)

    top_entries = _get_top_entries(entries, top)
    return top_entries


def _create_soup_obj(url):
    """Need utf-8 to properly parse emojis"""
    resp = requests.get(url)
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


def _get_title_tags(soup):
    title_tags = soup.find_all("span", class_="title")
    return title_tags


def _create_entry(title_tag):
    title = title_tag.text.strip()
    points, comments = _extract_points_and_comments(title_tag)
    entry = Entry(title, points, comments)
    return entry


def _extract_points_and_comments(title_tag):
    controls_tag = title_tag.find_next("span", class_="controls")
    point_comment_string = controls_tag.text.strip()

    points = re.match(r"(\d+) point", point_comment_string).group(1)
    comments = re.search(r"(\d+) comment", point_comment_string).group(1)

    return int(points), int(comments)


def _get_top_entries(entries, top):
    sorted_entries = sorted(entries, key=operator.itemgetter(1, 2), reverse=True)
    top_entries = sorted_entries[:top]
    return top_entries
