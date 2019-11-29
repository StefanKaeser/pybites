from numbers import Number


class IntList(list):
    def __init__(self, lst):
        super().__init__(self._to_ints(lst))

    def _to_int(self, arg):
        if isinstance(arg, Number) and (arg % 1 == 0):
            return int(arg)
        raise TypeError("Only integers are allowed")

    def _to_ints(self, args):
        return [self._to_int(arg) for arg in args]

    @property
    def mean(self):
        return sum(self) / len(self)

    @property
    def median(self):
        length = len(self)
        print(length)
        if length % 2 == 0:
            upper_median = sorted(self)[int(length / 2) - 1]
            lower_median = sorted(self)[int(length / 2)]
            return (upper_median + lower_median) / 2
        return sorted(self)[int(length / 2)]

    def append(self, arg):
        super().append(self._to_int(arg))

    def __add__(self, lst):
        return super().__add__(self._to_ints(lst))

    def __iadd__(self, lst):
        return super().__iadd__(self._to_ints(lst))
