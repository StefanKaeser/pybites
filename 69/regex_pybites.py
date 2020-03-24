import re


def has_timestamp(text):
    """Return True if text has a timestamp of this format:
       2014-07-03T23:30:37"""
    time_stamp_regex = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    return bool(re.search(time_stamp_regex, text))


def is_integer(number):
    """Return True if number is an integer"""
    return bool(re.fullmatch(r"-?\d+", str(number)))


def has_word_with_dashes(text):
    """Returns True if text has one or more words with dashes"""
    return bool(re.search(r"\w+-\w+", text))


def remove_all_parenthesis_words(text):
    """Return text but without any words or phrases in parenthesis:
       'Good morning (afternoon)' -> 'Good morning' (so don't forget
       leading spaces)"""
    return re.sub(r" +\(.*?\)", "", text)


def split_string_on_punctuation(text):
    """Split on ?!.,; - e.g. "hi, how are you doing? blabla" ->
       ['hi', 'how are you doing', 'blabla']
       (make sure you strip trailing spaces)"""
    return [str.strip() for str in re.split(r"[?!.,;]", text) if str]


def remove_duplicate_spacing(text):
    """Replace multiple spaces by one space"""
    return re.sub(" +", " ", text)


def has_three_consecutive_vowels(word):
    """Returns True if word has at least 3 consecutive vowels"""
    return bool(re.search(r"[aeuoi]{3,}", word, re.IGNORECASE))


def convert_emea_date_to_amer_date(date):
    """Convert dd/mm/yyyy (EMEA date format) to mm/dd/yyyy
       (AMER date format)"""
    time_stamp_re = r"(\d{2})/(\d{2})/(\d{4})"
    return re.sub(time_stamp_re, r"\2/\1/\3", date)
