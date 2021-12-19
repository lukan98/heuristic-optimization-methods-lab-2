import parser
import sys
import greedy_algorithm
import local_search_algorithm
import random_solution_algorithm
from Tabu import *

players = parser.parse_instance(sys.argv[1])

greedy_squad = greedy_algorithm.run(players)
file = open("greedy_solution.txt", "w")
first_team = list(map(lambda x: str(x.identifier), greedy_squad.first_team))
subs = list(map(lambda x: str(x.identifier), greedy_squad.substitutes))
file.write(",".join(first_team))
file.write("\n")
file.write(",".join(subs))
file.close()

# random_squad = random_solution_algorithm.run(players)
# file = open("random_solution.txt", "w")
# first_team = list(map(lambda x: str(x.identifier), random_squad.first_team))
# subs = list(map(lambda x: str(x.identifier), random_squad.substitutes))
# file.write(",".join(first_team))
# file.write("\n")
# file.write(",".join(subs))
# file.close()

tabu_search = TabuSearch(instance=players, starting_solution=greedy_squad, budget=100)
neighbors = tabu_search.generate_neighbors(greedy_squad)
tabu_search_result = tabu_search.run(250, verbose=True)
file = open("tabu_search.txt", "w")
first_team = list(map(lambda x: str(x.identifier), tabu_search_result.first_team))
subs = list(map(lambda x: str(x.identifier), tabu_search_result.substitutes))
file.write(",".join(first_team))
file.write("\n")
file.write(",".join(subs))
file.close()


local_iterations = 0
local_optimized_squad = greedy_squad
while local_search_algorithm.optimise(local_optimized_squad, 100.0, players):
    local_iterations += 1
file = open("local_optimised.txt", "w")
first_team = list(map(lambda x: str(x.identifier), local_optimized_squad.first_team))
subs = list(map(lambda x: str(x.identifier), local_optimized_squad.substitutes))
file.write(",".join(first_team))
file.write("\n")
file.write(",".join(subs))
file.close()