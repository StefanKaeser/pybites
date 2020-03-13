from string import ascii_uppercase
import itertools


def sequence_generator():
    def iterator():
        for number, letter in enumerate(ascii_uppercase, 1):
            yield number
            yield letter

    yield from itertools.cycle(iterator())
