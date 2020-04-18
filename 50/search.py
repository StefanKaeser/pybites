from collections import namedtuple
from datetime import datetime
from functools import partial


from dateutil.parser import parse as parse_timestamp
from time import mktime

import feedparser

FEED = "https://bites-data.s3.us-east-2.amazonaws.com/all.rss.xml"

Entry = namedtuple("Entry", "date title link tags")


def get_feed_entries(feed=FEED):
    """Use feedparser to parse PyBites RSS feed.
       Return a list of Entry namedtuples (date = date, drop time part)
    """
    feed = feedparser.parse(feed)
    entries = feed["entries"]

    entries = [_parse_entries(entry) for entry in entries]
    return entries


def _parse_entries(entry):
    date_ = _convert_struct_time_to_dt(entry["published_parsed"])
    title = entry["title"]
    link = entry["link"]
    tags = [tag["term"].lower() for tag in entry["tags"]]

    entry = Entry(date_, title, link, tags)
    return entry


def _convert_struct_time_to_dt(stime):
    """Convert a time.struct_time as returned by feedparser into a
    datetime.date object, so:
    time.struct_time(tm_year=2016, tm_mon=12, tm_mday=28, ...)
    -> date(2016, 12, 28)
    """
    timestamp = mktime(stime)
    dt = datetime.fromtimestamp(timestamp)
    return dt.date()


def filter_entries_by_tag(search, entry):
    """Check if search matches any tags as stored in the Entry namedtuple
       (case insensitive, only whole, not partial string matches).
       Returns bool: True if match, False if not.
       Supported searches:
       1. If & in search do AND match,
          e.g. flask&api should match entries with both tags
       2. Elif | in search do an OR match,
          e.g. flask|django should match entries with either tag
       3. Else: match if search is in tags
    """
    search = search.lower()

    if _multiple_symbols_in_search(search):
        raise NotImplementedError

    contained_symbol = _get_contained_symbol(search)
    search_words = search.split(contained_symbol)
    match_function = SYMBOL_TO_MATCHFUNCTION.get(contained_symbol, _all_in)

    source = entry.tags
    does_match = match_function(search_words, source)

    return does_match


def _multiple_symbols_in_search(search):
    symbols = SYMBOL_TO_MATCHFUNCTION.keys()
    contained_symbols = set(symbol for symbol in symbols if symbol in search)
    return len(contained_symbols) > 1


def _get_contained_symbol(search):
    symbols = SYMBOL_TO_MATCHFUNCTION.keys()
    for symbol in symbols:
        if symbol in search:
            return symbol


def _all_in(search_words, source):
    does_match = all(search_word in source for search_word in search_words)
    return does_match


def _atleast_one_in(search_words, source):
    does_match = any(search_word in source for search_word in search_words)
    return does_match


SYMBOL_TO_MATCHFUNCTION = {"&": _all_in, "|": _atleast_one_in}


def main():
    """Entry point to the program
       1. Call get_feed_entries and store them in entries
       2. Initiate an infinite loop
       3. Ask user for a search term:
          - if enter was hit (empty string), print 'Please provide a search term'
          - if 'q' was entered, print 'Bye' and exit/break the infinite loop
       4. Filter/match the entries (see filter_entries_by_tag docstring)
       5. Print the title of each match ordered by date ascending
       6. Secondly, print the number of matches: 'n entries matched'
          (use entry if only 1 match)
    """
    entries = get_feed_entries()

    while True:
        search_term = input("Enter a search term:")

        if search_term == "":
            print("Please provide a search term")
            continue
        elif search_term == "q":
            print("Bye")
            break

        filter_function = partial(filter_entries_by_tag, search_term)
        filtered_entries = list(filter(filter_function, entries))

        filtered_entries = sorted(filtered_entries, key=lambda x: x.date)
        for entry in filtered_entries:
            print(entry.title)

        number_of_matches = len(filtered_entries)

        print(
            f"{number_of_matches} {'entries' if number_of_matches != 1 else 'entry'} matched"
        )


if __name__ == "__main__":
    main()
