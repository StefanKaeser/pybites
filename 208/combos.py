import itertools


def find_number_pairs(numbers, N=10):
    return [pair for pair in itertools.combinations(numbers, r=2) if sum(pair) == N]
