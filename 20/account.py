class Account:

    def __init__(self):
        self._transactions = []

    @property
    def balance(self):
        return sum(self._transactions)

    def __add__(self, amount):
        self._transactions.append(amount)

    def __sub__(self, amount):
        self._transactions.append(-amount)

    def __enter__(self):
        self._transactions_backup = self._transactions.copy()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.balance < 0:
            self._transactions = self._transactions_backup
