from itertools import product


class Matrix(object):
    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return f'<Matrix values="{self.values}">'

    @property
    def nrows(self):
        return len(self.values)

    @property
    def ncolumns(self):
        return len(self.values[0])

    def __matmul__(self, other):
        if self.ncolumns != other.nrows:
            raise ValueError("None compatible matrices")

        result_values = [[0] * other.ncolumns for _ in range(self.nrows)]

        for nrow, ncolumn in product(range(self.nrows), range(other.ncolumns)):
            row = self.values[nrow]
            column = [row[ncolumn] for row in other.values]
            value = sum(
                [row_ele * column_ele for row_ele, column_ele in zip(row, column)]
            )
            result_values[nrow][ncolumn] = value

        return Matrix(result_values)

    # __rmatmul__ not necessary, because we can only multiply matrices anyways

    def __imatmul__(self, other):
        self.values = (self @ other).values

        return self
