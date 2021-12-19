import random

from models import *

budget = 100.0

max_gks = 2
max_defs = 5
max_mids = 5
max_fws = 3

max_players_per_club = 3

starting_gks = 1
min_starting_defs = 3
min_starting_fws = 1

substitute_gks = 1

clubs_filtered = set()
first_team_positions_filled = set()
squad_positions_filled = set()
prioritized_positions = set()


def run(players: [Player]) -> Squad:
    squad = Squad()
    max_price = budget

    def starter_filter(player: Player):
        return player.price <= max_price \
               and player not in squad.first_team + squad.substitutes \
               and player.club not in clubs_filtered \
               and player.position not in first_team_positions_filled \
               and player.position not in squad_positions_filled

    def substitute_filter(player: Player):
        return player.price <= max_price \
               and player not in squad.first_team + squad.substitutes \
               and player.club not in clubs_filtered \
               and player.position not in squad_positions_filled

    def find_cheaper_alternative_to_most_expensive() -> float:
        # assuming the most expensive player is in the first team
        most_expensive_player = squad.most_expensive_player()

        if most_expensive_player.club in clubs_filtered:
            clubs_filtered.remove(most_expensive_player.club)

        replacement_player_list = list(filter(lambda player:
                                              player.price < most_expensive_player.price
                                              and player.position == most_expensive_player.position
                                              and player not in squad.first_team + squad.substitutes,
                                              players))

        replacement_player = random.choice(replacement_player_list)

        squad.remove_from_team(most_expensive_player)
        squad.add_to_first_team(replacement_player)

        if squad.no_of_players_in_club(replacement_player.club) == 3:
            clubs_filtered.add(replacement_player.club)

        return most_expensive_player.price - replacement_player.price

    iterations = 0

    while len(squad.first_team) + len(squad.substitutes) < 15:

        iterations += 1

        if len(squad.first_team) < 11:
            # check if its time to fill out defender, forward or goalkeeper quotas
            if 11 - len(squad.first_team) <= starting_gks + min_starting_defs + min_starting_fws:
                if squad.no_of_starters_in_position(gk) < starting_gks:
                    prioritized_positions.add(gk)
                elif gk in prioritized_positions:
                    prioritized_positions.remove(gk)

                if squad.no_of_starters_in_position(df) < min_starting_defs:
                    prioritized_positions.add(df)
                elif df in prioritized_positions:
                    prioritized_positions.remove(df)

                if squad.no_of_starters_in_position(fw) < min_starting_fws:
                    prioritized_positions.add(fw)
                elif fw in prioritized_positions:
                    prioritized_positions.remove(fw)

            # check if there are affordable players
            if any(starter_filter(player) for player in players):
                selected_players = list(filter(starter_filter, players))
                selected_player = random.choice(selected_players)
                squad.add_to_first_team(selected_player)
                max_price -= selected_player.price

                if squad.no_of_players_in_club(selected_player.club) == max_players_per_club:
                    clubs_filtered.add(selected_player.club)

                if selected_player.position == gk and squad.no_of_starters_in_position(gk) == starting_gks:
                    first_team_positions_filled.add(gk)

                if selected_player.position == df and squad.no_of_players_in_position(df) == max_defs:
                    first_team_positions_filled.add(df)
                    squad_positions_filled.add(df)

                if selected_player.position == mf and squad.no_of_players_in_position(mf) == max_mids:
                    first_team_positions_filled.add(mf)
                    squad_positions_filled.add(mf)

                if selected_player.position == fw and squad.no_of_players_in_position(fw) == max_fws:
                    first_team_positions_filled.add(fw)
                    squad_positions_filled.add(fw)
            # no affordable players
            else:
                # assuming the most expensive player is in the first team
                savings = find_cheaper_alternative_to_most_expensive()
                max_price += savings

        # we're filling the substitutes
        else:
            if len(squad.substitutes) < 4:
                if 4 - len(squad.substitutes) == substitute_gks and squad.no_of_players_in_position(
                        gk) < substitute_gks:
                    prioritized_positions.add(gk)
                elif gk in prioritized_positions:
                    prioritized_positions.remove(gk)

            if any(substitute_filter(player) for player in players):
                selected_players = list(filter(substitute_filter, players))
                selected_player = random.choice(selected_players)
                squad.add_to_substitutes(selected_player)
                max_price -= selected_player.price

                if squad.no_of_players_in_club(selected_player.club) == max_players_per_club:
                    clubs_filtered.add(selected_player.club)

                if selected_player.position == gk and squad.no_of_subs_in_position(gk) == substitute_gks:
                    squad_positions_filled.add(gk)

                if selected_player.position == df and squad.no_of_players_in_position(df) == max_defs:
                    squad_positions_filled.add(df)

                if selected_player.position == mf and squad.no_of_players_in_position(mf) == max_mids:
                    squad_positions_filled.add(mf)

                if selected_player.position == fw and squad.no_of_players_in_position(fw) == max_fws:
                    squad_positions_filled.add(fw)

            # no affordable players
            else:
                # assuming the most expensive player is in the first team
                savings = find_cheaper_alternative_to_most_expensive()
                max_price += savings

    return squad
