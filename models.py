gk = "GK"
df = "DEF"
mf = "MID"
fw = "FW"


class Player:
    def __init__(self, identifier: int, position: str, name: str, club: str, points: float, price: float):
        self.identifier = identifier
        self.position = position
        self.name = name
        self.club = club
        self.points = points
        self.price = price


class Squad:
    first_team: [Player] = []
    substitutes: [Player] = []

    def no_of_players_in_position(self, position: str) -> int:
        return self.no_of_subs_in_position(position) + self.no_of_starters_in_position(position)

    def no_of_subs_in_position(self, position: str) -> int:
        return sum(1 for substitute in self.substitutes if substitute.position == position)

    def no_of_starters_in_position(self, position: str) -> int:
        return sum(1 for starter in self.first_team if starter.position == position)

    def no_of_players_in_club(self, club: str) -> int:
        return sum(1 for player in self.first_team + self.substitutes if player.club == club)

    def most_expensive_player(self) -> Player:
        sorted_by_price = sorted(self.first_team + self.substitutes, key=lambda player: player.price, reverse=True)
        return sorted_by_price[0]

    def remove_from_team(self, player: Player):
        if player in self.first_team:
            self.first_team.remove(player)
        elif player in self.substitutes:
            self.substitutes.remove(player)

    def add_to_first_team(self, player: Player):
        self.first_team.append(player)
        return

    def add_to_substitutes(self, player: Player):
        self.substitutes.append(player)
        return

    def least_efficient_starter(self) -> Player:
        sorted_by_efficiency = sorted(self.first_team, key=lambda player: player.points/player.price)
        return sorted_by_efficiency[0]

    def starters_by_lowest_efficiency(self) -> [Player]:
        return sorted(self.first_team, key=lambda player: player.points/player.price)