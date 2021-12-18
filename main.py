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

neighbors = tabu_search.generate_neighbors(squad)

tabu_search_result = tabu_search.run(500, verbose=True)

file = open("tabu_search.txt", "w")
first_team = list(map(lambda x: str(x.identifier), tabu_search_result.first_team))
subs = list(map(lambda x: str(x.identifier), tabu_search_result.substitutes))
file.write(",".join(first_team))
file.write("\n")
file.write(",".join(subs))
file.close()
