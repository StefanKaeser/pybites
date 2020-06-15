#import heapq
from collections import namedtuple

Path = namedtuple("Path", ["vertices", "distance"])


def shortest_path(graph, start, end):
    """
       Input: graph: a dictionary of dictionary
              start: starting city   Ex. a
              end:   target city     Ex. b

       Output: tuple of (distance, [path of cites])
       Ex.   (distance, ['a', 'c', 'd', 'b])
    """
    path = Path([start,], 0)
    paths = [path,]

    step = 1
    visited_vertices = [start,]
    while True:
        for path in paths:
            vertices, distance = path
            last_vertex = vertices[-1]
            relative_distance = step - distance

            connections = graph[last_vertex]
            for next_vertex, needed_distance in connections.items():
                not_already_visited = next_vertex not in visited_vertices 
                possible_connection = needed_distance <= relative_distance

                if not_already_visited and possible_connection:
                    new_path = Path(vertices + [next_vertex], step)
                    paths.append(new_path)

                    visited_vertices.append(next_vertex)

                    if next_vertex == end:
                        return (new_path.distance, new_path.vertices)
        step += 1
