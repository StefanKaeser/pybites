def num_ops(n):
    """
    Input: an integer number, the target number
    Output: the minimum number of operations required to reach to n from 1.

    Two operations rules:
    1.  multiply by 2
    2.  int. divide by 3

    The base number is 1. Meaning the operation will always start with 1
    These rules can be run in any order, and can be run independently.

    [Hint] the data structure is the key to solve it efficiently.
    """
    ops_num = 0

    seen_nodes = set()
    nodes = [1]
    while True:
        seen_nodes.update(nodes)
        nodes = get_new_nodes(nodes, seen_nodes)
        ops_num += 1
        if n in nodes:
            return ops_num

    return ops_num


def get_new_nodes(nodes, seen_nodes):
    new_nodes = set()
    for number in nodes:
        new_nodes.update(get_next_depth(number))
    new_nodes = new_nodes - seen_nodes
    return list(new_nodes)


def get_next_depth(number):
    nodes = []
    nodes.append(number * 2)
    if number >= 3:
        nodes.append(number // 3)
    return nodes
