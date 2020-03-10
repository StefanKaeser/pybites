import itertools


def friends_teams(friends, team_size=2, order_does_matter=False):
    if order_does_matter:
        get_teams = itertools.permutations
    else:
        get_teams = itertools.combinations
    return list(get_teams(friends, r=team_size))
