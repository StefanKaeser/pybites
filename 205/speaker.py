import re
from urllib.request import urlretrieve
from pathlib import Path

import gender_guesser.detector as gender
from bs4 import BeautifulSoup as Soup

TMP = Path("/tmp")
PYCON_HTML = TMP / "pycon2019.html"
PYCON_PAGE = "https://bites-data.s3.us-east-2.amazonaws.com/" "pycon2019.html"
NAME_SEPERATORS = [",", "/"]

if not PYCON_HTML.exists():
    urlretrieve(PYCON_PAGE, PYCON_HTML)


def get_pycon_speaker_first_names(soup=None):
    """Parse the PYCON_HTML using BeautifulSoup, extracting all
       speakers (class "speaker"). Note that some items contain
       multiple speakers so you need to extract them.
       Return a list of first names
    """
    if not soup:
        soup = _get_soup(html=PYCON_HTML)

    names = _get_speaker_names(soup)
    first_names = [name.split()[0] for name in names]
    return first_names


def _get_soup(html=PYCON_HTML):
    return Soup(html.read_text(encoding="utf-8"), "html.parser")


def _get_speaker_names(soup):
    span_tags = soup.find_all("span", class_="speaker")

    names = []
    for tag in span_tags:
        text = tag.text.strip()
        names += _extract_names(text)
    return names


def _extract_names(text, name_seperators=NAME_SEPERATORS):
    names = re.split(rf"[{''.join(name_seperators)}]", text)
    return [name.strip() for name in names]


def get_percentage_of_female_speakers(first_names):
    """Run gender_guesser on the names returning a percentage
       of female speakers (female and mostly_female),
       rounded to 2 decimal places."""
    number_of_names = len(first_names)
    number_of_female_names = _get_number_of_female_names(first_names)

    ratio = number_of_female_names / number_of_names
    return _ratio_to_percentage(ratio, decimal_places=2)


def _get_number_of_female_names(names):
    gender_detector = gender.Detector()
    female_names = [
        name
        for name in names
        if gender_detector.get_gender(name) in ["female", "mostly_female"]
    ]
    return len(female_names)


def _ratio_to_percentage(ratio, decimal_places):
    return round(100 * ratio, decimal_places)


if __name__ == "__main__":
    names = get_pycon_speaker_first_names()
    perc = get_percentage_of_female_speakers(names)
    print(perc)
