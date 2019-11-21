import random

BITES = {6: 'PyBites Die Hard',
         7: 'Parsing dates from logs',
         9: 'Palindromes',
         10: 'Practice exceptions',
         11: 'Enrich a class with dunder methods',
         12: 'Write a user validation function',
         13: 'Convert dict in namedtuple/json',
         14: 'Generate a table of n sequences',
         15: 'Enumerate 2 sequences',
         16: 'Special PyBites date generator',
         17: 'Form teams from a group of friends',
         18: 'Find the most common word',
         19: 'Write a simple property',
         20: 'Write a context manager',
         21: 'Query a nested data structure'}
bites_done = {6, 10, 16, 18, 21}


class NoBitesAvailable(Exception):
    pass


class Promo:

    def __init__(self, bites_done=bites_done):
        self.bites_done = bites_done

    def _pick_random_bite(self):
        # dict.keys() returns a ditc_key object which can be used with set
        bites_not_done = list(BITES.keys() - self.bites_done)
        if not bites_not_done:
            raise NoBitesAvailable
        return random.choice(bites_not_done)

    def new_bite(self):
        random_bite = self._pick_random_bite()
        self.bites_done.add(random_bite)
        return random_bite
