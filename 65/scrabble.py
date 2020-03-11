import itertools
import os
import urllib.request

# PREWORK
# TMP = os.getenv("TMP", "/tmp")
TMP = "."
DICT = "dictionary.txt"
DICTIONARY = os.path.join(TMP, DICT)
# urllib.request.urlretrieve(
#    f'https://bites-data.s3.us-east-2.amazonaws.com/{DICT}',
#    DICTIONARY
# )

with open(DICTIONARY) as f:
    dictionary = set([word.strip().lower() for word in f.read().split()])


def get_possible_dict_words(draw):
    """Get all possible words from a draw (list of letters) which are
       valid dictionary words. Use _get_permutations_draw and provided
       dictionary"""
    permutations = _get_permutations_draw(draw)
    words = set(["".join(perm).lower() for perm in permutations])
    return words & dictionary


def _get_permutations_draw(draw):
    """Helper to get all permutations of a draw (list of letters), hint:
       use itertools.permutations (order of letters matters)"""
    size_draw = len(draw)
    for size in range(1, size_draw + 1):
        yield from itertools.permutations(draw, size)
