from collections import namedtuple
from heapq import heappop, heappush

Path = namedtuple("Path", ["distance", "vertices"])


def shortest_path(graph, start, end):
    """
       Input: graph: a dictionary of dictionary
              start: starting city   Ex. a
              end:   target city     Ex. b

       Output: tuple of (distance, [path of cites])
       Ex.   (distance, ['a', 'c', 'd', 'b])
    """
    path = Path(0, [start,])
    paths = [path]

    visited_vertices = [start]
    while True:
        path = heappop(paths)

        distance, vertices = path
        last_vertex = vertices[-1]

        if last_vertex == end:
            return (path.distance, path.vertices)

        visited_vertices.append(last_vertex)

        connections = graph[last_vertex]
        for next_vertex, needed_distance in connections.items():
            not_already_visited = next_vertex not in visited_vertices
            if not_already_visited:
                new_path = Path(distance + needed_distance, vertices + [next_vertex])
                heappush(paths, new_path)
