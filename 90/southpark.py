from collections import Counter, defaultdict
import csv

import requests

CSV_URL = 'https://raw.githubusercontent.com/pybites/SouthParkData/master/by-season/Season-{}.csv' # noqa E501


def get_season_csv_file(season):
    """Receives a season int, and downloads loads in its
       corresponding CSV_URL"""
    with requests.Session() as s:
        download = s.get(CSV_URL.format(season))
        return download.content.decode('utf-8')


def get_num_words_spoken_by_character_per_episode(content):
    """Receives loaded csv content (str) and returns a dict of
       keys=characters and values=Counter object,
       which is a mapping of episode=>words spoken"""
    words_spoken_by_character_per_episode = defaultdict(Counter)

    directions = content.splitlines()[1:]
    directions_iter = iter(directions)
    for direction in directions_iter: 
        # A direction is ended with a '"' on the next line.
        next_direction = next(directions_iter)
        while next_direction != '"':
            direction += next_direction
            next_direction = next(directions_iter)

        _, episode, character, *lines = direction.split(",")
        line = "".join(lines)

        words = line.split(" ")
        words = [word for word in words if len(word) != 0]
        number_of_words = len(words)
        if character == "Ms. Choksondik" and episode == "10":
            print(direction)
            print(line)
            print(len(words))
        words_spoken_by_character_per_episode[character][episode] += number_of_words

    return words_spoken_by_character_per_episode


#words_spoken_by_character_per_episode = get_num_words_spoken_by_character_per_episode(get_season_csv_file(season=5))
#print(words_spoken_by_character_per_episode["Ms. Choksondik"].most_common())

