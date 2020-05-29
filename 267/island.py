# Hint:
# You can define a helper funtion: get_others(map, row, col) to assist you.
# Then in the main island_size function just call it when traversing the map.
import itertools
from collections import namedtuple

Position = namedtuple("Position", ["row", "column"])


def get_number_of_neighboring_islands(map_, position):
    """Go through the map and check the size of the island
       (= summing up all the 1s that are part of the island)

       Input - the map, row, column position
       Output - return the total numbe)
    """
    position_of_neighbors = get_position_of_neighbors(position)

    number_of_neighboring_islands = 0
    for position in position_of_neighbors:
        number_of_neighboring_islands += access_map(map_, position)

    return number_of_neighboring_islands


def get_position_of_neighbors(position):
    row, column = position
    top = Position(row - 1, column)
    bottom = Position(row + 1, column)
    left = Position(row, column - 1)
    right = Position(row, column + 1)

    position_of_neighbors = [top, bottom, left, right]
    return position_of_neighbors


def access_map(map_, position):
    max_row, max_column = get_max_row_and_max_column(map_)

    row, column = position
    if in_range(row, 0, max_row) and in_range(column, 0, max_column):
        return map_[row][column]
    else:
        return 0


def get_max_row_and_max_column(map_):
    max_row = len(map_)
    max_column = len(map_[0])
    return max_row, max_column


def in_range(value, min_, max_):
    return (value >= min_) and (value < max_)


def island_size(map_):
    """Hint: use the get_others helper

    Input: the map
    Output: the perimeter of the island
    """
    perimeter = 0
    for position in get_positions(map_):
        if is_island(map_, position):
            perimeter += get_perimeter_of_element(map_, position)

    return perimeter


def get_positions(map_):
    max_row, max_column = get_max_row_and_max_column(map_)
    positions = []
    for row, column in itertools.product(range(max_row), range(max_column)):
        positions.append(Position(row, column))
    return positions


def is_island(map_, position):
    return access_map(map_, position) == 1


def get_perimeter_of_element(map_, position):
    perimeter_per_element = 4
    number_of_neighboring_islands = get_number_of_neighboring_islands(map_, position)
    return perimeter_per_element - number_of_neighboring_islands
