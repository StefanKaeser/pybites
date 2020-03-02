import json
import re


NOMINATION_REGEXS = [
    r"\d+ wins & (\d+) nominations.",
    r"Nominated for (\d+) Oscar. Another \d+ wins & (\d+) nominations.",
]


def get_movie_data(files: list) -> list:
    """Parse movie json files into a list of dicts"""
    movies = []
    for file_ in files:
        with open(file_, "r") as f:
            movie = json.load(f)
        movies.append(movie)
    return movies


def get_single_comedy(movies: list) -> str:
    """return the movie with Comedy in Genres"""
    return [movie["Title"] for movie in movies if "comedy" in movie["Genre"].lower()][0]


def _get_nominations(movie):
    for regex in NOMINATION_REGEXS:
        match = re.match(regex, movie["Awards"])
        if match:
            nominations = sum([int(group) for group in match.groups()])
            return nominations


def get_movie_most_nominations(movies: list) -> str:
    """Return the movie that had the most nominations"""
    return max(movies, key=lambda x: _get_nominations(x))["Title"]


def _get_runtime(movie):
    return int(movie["Runtime"].split()[0])


def get_movie_longest_runtime(movies: list) -> str:
    """Return the movie that has the longest runtime"""
    return max(movies, key=lambda x: _get_runtime(x))["Title"]
