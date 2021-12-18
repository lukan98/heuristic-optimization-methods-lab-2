from models import *


def optimise(squad: Squad, budget: float, players: [Player]) -> bool:
    spent = sum(map(lambda player: player.price, squad.first_team + squad.substitutes))
    clubs_filtered = set()

    # find clubs to filter
    for club in list(map(lambda x: x.club, squad.first_team + squad.substitutes)):
        if list(map(lambda x: x.club, squad.first_team + squad.substitutes)).count(club) == 3:
            clubs_filtered.add(club)

    players_by_points_descending = sorted(players, key=lambda player: (player.points, -player.price), reverse=True)
    players_by_efficiency_descending = sorted(players, key=lambda player: player.points / player.price, reverse=True)

    def efficiency_filter(player: Player, player_to_replace: Player):
        return \
            (player.club not in clubs_filtered or player.club == player_to_replace.club)\
            and player.points / player.price >= player_to_replace.points / player_to_replace.price\
            and player.price < player_to_replace.price\
            and player.position == player_to_replace.position\
            and player not in squad.first_team + squad.substitutes

    def points_filter(player: Player, player_to_replace: Player):
        return \
            (player.club not in clubs_filtered or player.club == player_to_replace.club)\
            and player.points > player_to_replace.points\
            and player.price <= budget - spent + player_to_replace.price\
            and player.position == player_to_replace.position\
            and player not in squad.first_team + squad.substitutes

    def find_more_efficient_alternative(player_to_replace: Player) -> Player:
        if any(efficiency_filter(player, player_to_replace) for player in players_by_efficiency_descending):
            replacement = list(filter(lambda x: efficiency_filter(x, player_to_replace),
                                      players_by_efficiency_descending))[0]
            return replacement
        else:
            return player_to_replace

    def find_better_alternative(player_to_replace: Player) -> Player:
        if any(points_filter(player, player_to_replace) for player in players_by_points_descending):
            replacement = list(filter(lambda x: points_filter(x, player_to_replace),
                                      players_by_points_descending))[0]

            return replacement
        else:
            return player_to_replace

    for starter in squad.starters_by_lowest_efficiency():
        # DIFFERENCE COMPARED TO THE CODE POSTED ON MOODLE
        for club in list(map(lambda x: x.club, squad.first_team + squad.substitutes)):
            if list(map(lambda x: x.club, squad.first_team + squad.substitutes)).count(club) == 3:
                clubs_filtered.add(club)
        # DIFFERENCE COMAPRED TO THE CODE POSTED ON MOODLE

        spent = sum(map(lambda player: player.price, squad.first_team + squad.substitutes))
        replacement = find_more_efficient_alternative(starter)

        if replacement == starter:
            continue

        squad.remove_from_team(starter)

        spent -= starter.price

        if starter.club in clubs_filtered:
            clubs_filtered.remove(starter.club)

        if squad.no_of_players_in_club(replacement.club) == 2:
            clubs_filtered.add(replacement.club)

        squad.add_to_first_team(replacement)
        spent += replacement.price
        point_loss = starter.points - replacement.points

        # replacement SOMEHOW has more points than the original player revert and continue with the loop
        if point_loss < 0:
            squad.remove_from_team(replacement)
            squad.add_to_first_team(starter)
            continue

        for player in squad.first_team:
            potential_replacement = find_better_alternative(player)

            if potential_replacement == player:
                continue

            if potential_replacement.points - player.points > point_loss:
                squad.remove_from_team(player)

                if player.club in clubs_filtered:
                    clubs_filtered.remove(player.club)

                if squad.no_of_players_in_club(potential_replacement.club) == 2:
                    clubs_filtered.add(potential_replacement.club)

                squad.add_to_first_team(potential_replacement)
                return True

        # revert changes
        squad.remove_from_team(replacement)
        squad.add_to_first_team(starter)