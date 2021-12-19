import math
import random
from models import *

TABU_TENURE = int(math.sqrt(250))


class TabuMove:

    def __init__(self, solution: Squad):
        self.solution = solution
        self.tenure = TABU_TENURE


class TabuSearch:
    tolerance = 0.3

    def __init__(self, instance: [Player], starting_solution: Squad, budget: float):
        self.instance = instance
        self.player_dictionary = {player.identifier: player for player in instance}
        self.initial_solution = starting_solution
        self.budget = budget
        self.players_by_points_descending = sorted(instance,
                                                   key=lambda player: (player.points, -player.price), reverse=True)
        self.players_by_efficiency_descending = sorted(instance,
                                                       key=lambda player: player.points / player.price,
                                                       reverse=True)
        self.tabu_list: [TabuMove] = []

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

    def run(self, iterations: int, verbose=False) -> Squad:
        self.tabu_list.append(TabuMove(solution=self.initial_solution))
        best_solution = self.initial_solution
        current_solution = self.initial_solution

        for iteration in range(iterations):
            if verbose:
                print("Iteration: " + str(iteration) + ", best neighbor: " + str(current_solution.get_total_points()))

            tabu_squads = list(map(lambda tabu: tabu.solution, self.tabu_list))
            neighbors = self.generate_neighbors(current_solution)

            best_neighbor = None
            for neighbor in neighbors:
                if neighbor in tabu_squads:
                    continue

                if best_neighbor is None:
                    best_neighbor = neighbor

                neighbor_value = neighbor.get_total_points()
                if neighbor_value > best_solution.get_total_points():
                    best_solution = neighbor

                if neighbor_value > best_neighbor.get_total_points():
                    best_neighbor = neighbor

            current_solution = best_neighbor
            self.update_tabu_list()
            self.tabu_list.append(TabuMove(solution=best_neighbor))

        return best_solution

    def update_tabu_list(self):
        for tabu_move in self.tabu_list:
            tabu_move.tenure -= 1
            if tabu_move.tenure < 0:
                self.tabu_list.remove(tabu_move)

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
                second_neighbor_starters = list(map(lambda starter_id: self.player_dictionary[starter_id],
                                                    second_neighbor_starter_ids))
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
