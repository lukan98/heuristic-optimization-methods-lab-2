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
    first_team: [Player]
    substitutes: [Player]

    def __init__(self, first_team=None, substitutes=None):
        if substitutes is None:
            substitutes = []
        if first_team is None:
            first_team = []
        self.first_team = first_team
        self.substitutes = substitutes

    def __eq__(self, other):
        if isinstance(other, Squad):
            player_ids = list(map(lambda x: x.identifier, self.first_team + self.substitutes))
            other_player_ids = list(map(lambda x: x.identifier, other.first_team + other.substitutes))
            return all(player_id in player_ids for player_id in other_player_ids)
        else:
            return False

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
        sorted_by_efficiency = sorted(self.first_team, key=lambda player: player.points / player.price)
        return sorted_by_efficiency[0]

    def starters_by_lowest_efficiency(self) -> [Player]:
        return sorted(self.first_team, key=lambda player: player.points / player.price)

    def get_club_avoidlist(self, max_num=3) -> [str]:
        club_avoidlist = []
        for club in list(map(lambda x: x.club, self.first_team + self.substitutes)):
            if list(map(lambda x: x.club, self.first_team + self.substitutes)).count(club) == 3:
                club_avoidlist.append(club)

        return club_avoidlist

    def get_total_price(self) -> float:
        return sum(map(lambda x: x.price, self.first_team + self.substitutes))

    def get_total_points(self) -> float:
        return sum(map(lambda x: x.points, self.first_team))