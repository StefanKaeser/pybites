import os
import random
import string

import pytest

from movies import MovieDb

DB = os.path.join(os.getcwd(), f"movies.db")
# https://www.imdb.com/list/ls055592025/
DATA = [
    ("The Godfather", 1972, 9.2),
    ("The Shawshank Redemption", 1994, 9.3),
    ("Schindler's List", 1993, 8.9),
    ("Raging Bull", 1980, 8.2),
    ("Casablanca", 1942, 8.5),
    ("Citizen Kane", 1941, 8.3),
    ("Gone with the Wind", 1939, 8.1),
    ("The Wizard of Oz", 1939, 8),
    ("One Flew Over the Cuckoo's Nest", 1975, 8.7),
    ("Lawrence of Arabia", 1962, 8.3),
]
TABLE = "movies"


@pytest.fixture
def db():
    movies = MovieDb(db=DB, data=DATA, table=TABLE)
    movies.init()
    yield movies
    movies.drop_table()


def test_query_no_args(db):
    result = db.query()
    assert result == [
        (1, "The Godfather", 1972, 9.2),
        (2, "The Shawshank Redemption", 1994, 9.3),
        (3, "Schindler's List", 1993, 8.9),
        (4, "Raging Bull", 1980, 8.2),
        (5, "Casablanca", 1942, 8.5),
        (6, "Citizen Kane", 1941, 8.3),
        (7, "Gone with the Wind", 1939, 8.1),
        (8, "The Wizard of Oz", 1939, 8.0),
        (9, "One Flew Over the Cuckoo's Nest", 1975, 8.7),
        (10, "Lawrence of Arabia", 1962, 8.3),
    ]


@pytest.mark.parametrize(
    "title, expected",
    [
        ("The Godfather", [(1, "The Godfather", 1972, 9.2)]),
        ("Citizen Kane", [(6, "Citizen Kane", 1941, 8.3)]),
        ("citizen kane", [(6, "Citizen Kane", 1941, 8.3)]),
    ],
)
def test_query_title(db, title, expected):
    result = db.query(title=title)
    assert result == expected


@pytest.mark.parametrize(
    "year, expected",
    [
        ("1972", [(1, "The Godfather", 1972, 9.2)]),
        ("1941", [(6, "Citizen Kane", 1941, 8.3)]),
        (
            "1939",
            [(7, "Gone with the Wind", 1939, 8.1), (8, "The Wizard of Oz", 1939, 8.0)],
        ),
    ],
)
def test_query_year(db, year, expected):
    result = db.query(year=year)
    assert result == expected


@pytest.mark.parametrize(
    "score_gt, expected",
    [
        ("10.0", []),
        (
            "9.0",
            [
                (1, "The Godfather", 1972, 9.2),
                (2, "The Shawshank Redemption", 1994, 9.3),
            ],
        ),
        (
            "8.5",
            [
                (1, "The Godfather", 1972, 9.2),
                (2, "The Shawshank Redemption", 1994, 9.3),
                (3, "Schindler's List", 1993, 8.9),
                (9, "One Flew Over the Cuckoo's Nest", 1975, 8.7),
            ],
        ),
    ],
)
def test_query_score_gt(db, score_gt, expected):
    result = db.query(score_gt=score_gt)
    assert result == expected


@pytest.mark.parametrize(
    "title, year, score_gt, expected",
    [
        ("Raging Bull", 1941, 9.2, [(4, "Raging Bull", 1980, 8.2)]),
        (None, 1941, 9.2, [(6, "Citizen Kane", 1941, 8.3)]),
        (None, None, 9.2, [(2, "The Shawshank Redemption", 1994, 9.3)]),
    ],
)
def test_query_elifs(db, title, year, score_gt, expected):
    result = db.query(title=title, year=year, score_gt=score_gt)
    assert result == expected


def test_add(db):
    test_movie1 = ("Test the Movie", 2020, 10.0)
    lastrowid = db.add(*test_movie1)
    result = db.query(title=test_movie1[0])
    assert lastrowid == 11
    assert result == [(11,) + test_movie1]

    test_movie2 = ("Test the Movie 2", 2020, 10.0)
    lastrowid = db.add(*test_movie2)
    result = db.query(year=test_movie2[1])
    assert lastrowid == 12
    assert result == [(11,) + test_movie1, (12,) + test_movie2]


def test_delete(db):
    db.delete(4)
    result = db.query(title="Raging Bull")
    assert result == []

