import numbers


class Account:
    def __init__(self, name, start_balance=0):
        self.name = name
        self.start_balance = start_balance
        self._transactions = []

    @property
    def balance(self):
        return self.start_balance + sum(self._transactions)

    #  add dunder methods below
    def __len__(self):
        return len(self._transactions)

    def __lt__(self, acc2):
        return self.balance < acc2.balance

    def __le__(self, acc2):
        return self.balance <= acc2.balance

    def __eq__(self, acc2):
        return self.balance == acc2.balance

    __neq__ = not __eq__

    def __re__(self, acc2):
        return self.balance >= acc2.balance

    __rt__ = not __lt__

    def __getitem__(self, index):
        return self._transactions[index]

    def __iter__(self):
        return iter(self._transactions)

    def __add__(self, value):
        if not isinstance(value, numbers.Number):
            raise ValueError
        self._transactions.append(value)

    def __sub__(self, value):
        if not isinstance(value, numbers.Number):
            raise ValueError
        self._transactions.append(-value)

    def __str__(self):
        return f"{self.name} account - balance: {self.balance}"
