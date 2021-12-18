import csv
from models import Player


def parse_instance(source_string: str) -> [Player]:
    instance = open(file=source_string, mode="r", encoding="cp1252")
    reader = csv.reader(instance)
    players = []

    for player_row in reader:
        players.append(Player(
            identifier=int(player_row[0]),
            position=player_row[1],
            name=player_row[2],
            club=player_row[3],
            points=float(player_row[4]),
            price=float(player_row[5])))

    return players