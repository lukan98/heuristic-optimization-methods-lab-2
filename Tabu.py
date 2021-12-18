import random
from models import *


class Solution:

    def __init__(self, squad: Squad, points: float, price: float):
        self.squad = squad
        self.points = points
        self.price = price


class TabuMove:

    def __init__(self, solution: Solution):
        self.solution = solution
        self.tenure = 0


class TabuSearch:
    tolerance = 0.8

    def __init__(self, instance: [Player], starting_solution: Squad, budget: float):
        self.instance = instance
        self.player_dictionary = {player.identifier: player for player in instance}
        self.current_solution = starting_solution
        self.best_solution = starting_solution
        self.budget = budget
        self.players_by_points_descending = sorted(instance,
                                                   key=lambda player: (player.points, -player.price), reverse=True)
        self.players_by_efficiency_descending = sorted(instance,
                                                       key=lambda player: player.points / player.price,
                                                       reverse=True)

    def efficiency_filter(
            self,
            player: Player,
            player_to_replace: Player,
            squad: Squad
    ) -> bool:
        club_avoidlist = squad.get_club_avoidlist()
        return \
            (player.club not in club_avoidlist or player.club == player_to_replace.club) \
            and player.points / player.price >= player_to_replace.points / player_to_replace.price * self.tolerance \
            and player.price < player_to_replace.price \
            and player.position == player_to_replace.position \
            and player not in squad.first_team + squad.substitutes

    def find_more_efficient_alternative(self, player_to_replace: Player, squad: Squad) -> Player:
        if any(self.efficiency_filter(player, player_to_replace, squad) for player in
               self.players_by_efficiency_descending):
            replacement_list = list(filter(lambda x: self.efficiency_filter(x, player_to_replace, squad),
                                           self.players_by_efficiency_descending))
            return random.choice(replacement_list)
        else:
            return player_to_replace

    def points_filter(
            self,
            player: Player,
            player_to_replace: Player,
            squad: Squad
    ) -> bool:
        club_avoidlist = squad.get_club_avoidlist()
        spent = squad.get_total_price()
        return \
            (player.club not in club_avoidlist or player.club == player_to_replace.club) \
            and player.points > player_to_replace.points * self.tolerance \
            and player.price <= self.budget - spent + player_to_replace.price \
            and player.position == player_to_replace.position \
            and player not in squad.first_team + squad.substitutes

    def find_absolute_better_alternative(self, player_to_replace: Player, squad: Squad) -> Player:
        if any(self.points_filter(player, player_to_replace, squad) for player in self.players_by_points_descending):
            replacement_list = list(filter(lambda x: self.points_filter(x, player_to_replace, squad),
                                           self.players_by_points_descending))
            return random.choice(replacement_list)
        else:
            return player_to_replace

    def run_search(self):
        pass

    def generate_neighbors(self, squad: Squad) -> [Squad]:
        first_neighbors = []
        for player in squad.first_team:
            neighbor_starter_ids = self.destroy(squad, player)
            neighbor_starters = list(map(lambda starter_id: self.player_dictionary[starter_id], neighbor_starter_ids))
            first_neighbors.append(Squad(first_team=neighbor_starters, substitutes=squad.substitutes))

        neighbors = []
        for first_neighbor in first_neighbors:
            for player in first_neighbor.first_team:
                second_neighbor_starter_ids = self.repair(first_neighbor, player)
                second_neighbor_starters = list(map(lambda starter_id: self.player_dictionary[starter_id], second_neighbor_starter_ids))
                neighbors.append(Squad(first_team=second_neighbor_starters, substitutes=squad.substitutes))

        return neighbors

    def destroy(self, squad: Squad, player: Player) -> [int]:
        new_squad = list(map(lambda starter: starter.identifier, squad.first_team))
        replacement = self.find_more_efficient_alternative(player_to_replace=player, squad=squad)
        new_squad.remove(player.identifier)
        new_squad.append(replacement.identifier)
        return new_squad

    def repair(self, squad: Squad, player: Player):
        new_squad = list(map(lambda starter: starter.identifier, squad.first_team))
        replacement = self.find_absolute_better_alternative(player_to_replace=player, squad=squad)
        new_squad.remove(player.identifier)
        new_squad.append(replacement.identifier)
        return new_squad
