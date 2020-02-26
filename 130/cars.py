from collections import Counter

import requests

CAR_DATA = "https://bites-data.s3.us-east-2.amazonaws.com/cars.json"

# pre-work: load JSON data into program

with requests.Session() as s:
    data = s.get(CAR_DATA).json()


def most_prolific_automaker(year):
    """Given year 'year' return the automaker that released
       the highest number of new car models"""
    automakers = [car['automaker'] for car in data if car['year'] == year]
    automaker_counter = Counter(automakers)

    try:
        return automaker_counter.most_common(1)[0][0]
    except IndexError:
        raise ValueError("There were no cars produced in this year.")


def get_models(automaker, year):
    """Filter cars 'data' by 'automaker' and 'year',
       return a set of models (a 'set' to avoid duplicate models)"""
    models = set(
        [
            car["model"]
            for car in data
            if car["automaker"] == automaker and car["year"] == year
        ]
    )
    return models
