import parser
import sys
import greedy_algorithm
import local_search_algorithm
from Tabu import *

players = parser.parse_instance(sys.argv[1])

squad = greedy_algorithm.run(players)

file = open("greedy_solution.txt", "w")
first_team = list(map(lambda x: str(x.identifier), squad.first_team))
subs = list(map(lambda x: str(x.identifier), squad.substitutes))
file.write(",".join(first_team))
file.write("\n")
file.write(",".join(subs))
file.close()

local_iterations = 0
while local_search_algorithm.optimise(squad, 100.0, players):
    local_iterations += 1

file = open("local_optimised.txt", "w")
first_team = list(map(lambda x: str(x.identifier), squad.first_team))
subs = list(map(lambda x: str(x.identifier), squad.substitutes))
file.write(",".join(first_team))
file.write("\n")
file.write(",".join(subs))
file.close()

tabu_search = TabuSearch(instance=players, starting_solution=squad, budget=100)
neighborhood = tabu_search.generate_neighbors(squad)

best_neighbor = squad
for neighbor in neighborhood:
    if neighbor.get_total_points() > squad.get_total_points():
        best_neighbor = neighbor

for starter in best_neighbor.first_team:
    print(str(starter.identifier))