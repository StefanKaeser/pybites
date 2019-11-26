from collections import namedtuple
from datetime import datetime

Transaction = namedtuple("Transaction", "giver points date")
Transaction.__new__.__defaults__ = (datetime.now(),)  # http://bit.ly/2rmiUrL


class User:
    def __init__(self, name):
        self.name = name
        self._transactions = []

    def __add__(self, other):
        if type(other) != Transaction:
            raise TypeError(
                "Can only add objects of type %r to a %r." % (Transaction, User)
            )
        self._transactions.append(other)

    @property
    def points(self):
        return [transaction.points for transaction in self._transactions]

    @property
    def karma(self):
        return sum(self.points)

    @property
    def fans(self):
        # Use set comprehension
        return len({transaction.giver for transaction in self._transactions})

    def __str__(self):
        # Use if else condition in f-string to get singular or plural
        return (
            f"{self.name} has a karma of {self.karma} and {self.fans}"
            f" fan{'s' if self.fans != 1 else ''}"
        )
