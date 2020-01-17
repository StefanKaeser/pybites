from datetime import datetime
import json
import os
from pathlib import Path
from urllib.request import urlretrieve

import pytest

from zodiac import (
    get_signs,
    get_sign_with_most_famous_people,
    signs_are_mutually_compatible,
    get_sign_by_date,
)

# original source: https://zodiacal.herokuapp.com/api
URL = "https://bites-data.s3.us-east-2.amazonaws.com/zodiac.json"
# TMP = os.getenv("TMP", "/tmp")
TMP = "./"
PATH = Path(TMP, "zodiac.json")


@pytest.fixture(scope="module")
def signs():
    if not PATH.exists():
        urlretrieve(URL, PATH)
    with open(PATH) as f:
        data = json.loads(f.read())
    return get_signs(data)


def test_sign_class(signs):
    assert "zodiac.Sign" in str(type(signs[0]))


def test_get_sign_with_most_famous_people(signs):
    result = get_sign_with_most_famous_people(signs)
    assert result == ("Scorpio", 35)


def test_mutually_compatible(signs):
    result = signs_are_mutually_compatible(signs, "Aries", "Leo")
    assert result == True
    result = signs_are_mutually_compatible(signs, "Leo", "Aries")
    assert result == True


def test_not_mutually_compatible(signs):
    result = signs_are_mutually_compatible(signs, "Aries", "Cancer")
    assert result == False
    result = signs_are_mutually_compatible(signs, "Cancer", "Aries",)
    assert result == False


@pytest.mark.parametrize(
    "date, expected_sign",
    [
        (datetime(year=1, month=4, day=18), "Aries"),
        (datetime(year=1, month=4, day=19), "Aries"),
        (datetime(year=1, month=4, day=20), "Taurus"),
        (datetime(year=1, month=3, day=22), "Aries"),
        (datetime(year=1, month=3, day=21), "Aries"),
        (datetime(year=1, month=3, day=20), "Pisces"),
    ],
)
def test_get_sign_by_date(signs, date, expected_sign):
    sign = get_sign_by_date(signs, date)
    assert sign == expected_sign


print([(s.name, s.sun_dates) for s in signs()])
