import itertools


def get_grid_dimensions(grid):
    nrows = len(grid)
    ncols = len(grid[0])
    if not len(set([len(row) for row in grid])) == 1:
        raise ValueError("The rows are not of equal length.")

    return nrows, ncols


def find_neighbors(square, grid):
    nrows, ncols = get_grid_dimensions(grid)
    row, col = square
    left = (row, col - 1)
    right = (row, col + 1)
    top = (row - 1, col)
    bottom = (row + 1, col)

    neighbors = [left, right, top, bottom]
    neighbors = (
        neighbor
        for neighbor in neighbors
        if (0 <= neighbor[0] < nrows) and (0 <= neighbor[1] < ncols)
    )
    return neighbors


def mark_island(square, grid):
    """
    Input: the row, column and grid
    Output: None. Just mark the visisted islands as in-place operation.
    """
    row, col = square
    grid[row][col] = "#"

    neighbors = find_neighbors(square, grid)
    for neighbor in neighbors:
        if is_island(neighbor, grid):
            mark_island(neighbor, grid)


def is_island(square, grid):
    row, col = square
    return grid[row][col] == 1


def count_islands(grid):
    """
    Input: 2D matrix, each item is [x, y] -> row, col.
    Output: number of islands, or 0 if found none.
    Notes: island is denoted by 1, ocean by 0 islands is counted by continously
        connected vertically or horizontically  by '1's.
    It's also preferred to check/mark the visited islands:
    - eg. using the helper function - mark_islands().
    """
    nrows, ncols = get_grid_dimensions(grid)

    nislands = 0
    for square in itertools.product(range(nrows), range(ncols)):
        if is_island(square, grid):
            nislands += 1
            mark_island(square, grid)
    return nislands
