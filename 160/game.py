import csv
import os
from urllib.request import urlretrieve

# TMP = os.getenv("TMP", "/tmp")
DATA = "battle-table.csv"
BATTLE_DATA = os.path.join(".", DATA)
if not os.path.isfile(BATTLE_DATA):
    urlretrieve(f"https://bites-data.s3.us-east-2.amazonaws.com/{DATA}", BATTLE_DATA)


def _create_defeat_mapping():
    """Parse battle-table.csv building up a defeat_mapping dict
       with keys = attackers / values = who they defeat.
    """
    with open(BATTLE_DATA) as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    defenders = rows[0][1:]

    wins_against_mapping = {}
    for row in rows[1:]:
        attacker, *outcomes = row
        wins_against = [
            defender
            for defender, outcome in zip(defenders, outcomes)
            if outcome == "win"
        ]
        wins_against_mapping[attacker] = wins_against
    return wins_against_mapping


def get_winner(player1, player2, defeat_mapping=None):
    """Given player1 and player2 determine game output returning the
       appropriate string:
       Tie
       Player1
       Player2
       (where Player1 and Player2 are the names passed in)

       Raise a ValueError if invalid player strings are passed in.
    """
    defeat_mapping = defeat_mapping or _create_defeat_mapping()

    if player1 not in defeat_mapping or player2 not in defeat_mapping:
        raise ValueError(
            f"Either {player1} or {player2} are not valid items in the game. "
            f"The game contains the following items: {', '.join(defeat_mapping.keys())}."
        )

    player1_wins = player2 in defeat_mapping[player1]
    player2_wins = player1 in defeat_mapping[player2]

    if player1_wins:
        return player1
    elif player2_wins:
        return player2
    else:
        return "Tie"
