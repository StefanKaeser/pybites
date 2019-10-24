import csv
from collections import defaultdict, namedtuple
import os
from urllib.request import urlretrieve

BASE_URL = 'http://projects.bobbelderbos.com/pcc/movies/'
TMP = ''

fname = 'movie_metadata.csv'
remote = os.path.join(BASE_URL, fname)
local = os.path.join(TMP, fname)
#urlretrieve(remote, local)

#MOVIE_DATA = local
MOVIE_DATA = "./movie_metadata.csv"
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')

def get_movies_by_director():
    """Extracts all movies from csv and stores them in a dict,
    where keys are directors, and values are a list of movies,
    use the defined Movie namedtuple"""
    movies_by_director = defaultdict(list)

    with open(MOVIE_DATA, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for movie_metadata in reader:
            director_name = movie_metadata['director_name']
            title = movie_metadata['movie_title'].replace(u'\xa0', '')
            try:
                year = int(movie_metadata['title_year'])
                #Discard any movies older than 1960.
                if year < MIN_YEAR:
                    continue
            except ValueError: # For some movies title year is not given.
                year = movie_metadata['title_year']
            score = float(movie_metadata['imdb_score'])
            
            movie = Movie(title=title, year=year, score=score)
            movies_by_director[director_name].append(movie)

    return movies_by_director

def calc_mean_score(movies):
    """Helper method to calculate mean of list of Movie namedtuples,
       round the mean to 1 decimal place"""
    scores = [movie.score for movie in movies]
    avg_score = sum(scores) / len(scores)
    avg_score = round(avg_score, 1)
    return avg_score
    
def get_average_scores(director_movies):
    """Iterate through the directors dict (returned by get_movies_by_director),
       return a list of tuples (director, average_score) ordered by highest
       score in descending order. Only take directors into account
       with >= MIN_MOVIES"""
    scores = []
    for director, movies in director_movies.items():
        if len(movies) < MIN_MOVIES:
            continue
        avg_score = calc_mean_score(movies)
        scores.append((director, avg_score))
    scores = sorted(scores, reverse=True, key=lambda x : x[1])
    return scores
