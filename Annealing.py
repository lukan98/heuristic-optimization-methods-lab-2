import math
import random
from models import *


class SimulatedAnnealing:
    tolerance = 0.3

    def __init__(self,
                 instance: [Player],
                 starting_solution: Squad,
                 budget: float,
                 initial_temperature: float,
                 cooling_schedule):
        self.instance = instance
        self.player_dictionary = {player.identifier: player for player in instance}
        self.initial_solution = starting_solution
        self.budget = budget
        self.players_by_points_descending = sorted(instance,
                                                   key=lambda player: (player.points, -player.price), reverse=True)
        self.players_by_efficiency_descending = sorted(instance,
                                                       key=lambda player: player.points / player.price,
                                                       reverse=True)
        self.initial_temperature = initial_temperature
        self.cooling_schedule = cooling_schedule

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

    def run(self, verbose=False) -> Squad:
        current_solution = self.initial_solution
        best_solution = self.initial_solution
        temperature = self.initial_temperature

        while temperature > 1e-100:
            neighbor = self.generate_neighbor(current_solution)
            neighbor_value = neighbor.get_total_points()
            current_value = current_solution.get_total_points()

            if neighbor_value > current_value:
                current_solution = neighbor

            elif neighbor_value <= current_value and random.random() < self.acceptance_probability(temperature, current_solution, neighbor):
                current_solution = neighbor

            if neighbor_value > best_solution.get_total_points():
                best_solution = neighbor

            temperature = self.cooling_schedule(temperature)

            if verbose:
                print("Temperature: " + str(temperature) + ", incumbent: " + str(current_solution.get_total_points()))

        return best_solution

    def acceptance_probability(
            self,
            temperature: float,
            incumbent_solution: Squad,
            neighboring_solution: Squad
    ) -> float:
        incumbent_value = incumbent_solution.get_total_points()
        neighboring_value = neighboring_solution.get_total_points()

        return math.exp(-(abs(incumbent_value - neighboring_value)) / temperature)

    def generate_neighbor(self, squad: Squad) -> Squad:
        neighbor = squad

        while squad == neighbor:
            # Destroy
            player_to_replace = random.choice(squad.first_team)
            neighbor_starter_ids = self.destroy(squad, player_to_replace)
            neighbor_starters = list(map(lambda starter_id: self.player_dictionary[starter_id], neighbor_starter_ids))
            first_neighbor = Squad(first_team=neighbor_starters, substitutes=squad.substitutes)

            # Repair
            player_to_replace = random.choice(first_neighbor.first_team)
            neighbor_starter_ids = self.repair(first_neighbor, player_to_replace)
            neighbor_starters = list(map(lambda starter_id: self.player_dictionary[starter_id], neighbor_starter_ids))
            neighbor = Squad(first_team=neighbor_starters, substitutes=first_neighbor.substitutes)

        return neighbor

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
