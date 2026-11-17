# Fantasy Football Team Selection — Local Search, SA and Tabu Search (HOM Lab 2)

A Python program that solves the fantasy-football squad-selection problem with several heuristic algorithms. It was written for the **Heuristic Optimization Methods (HOM)** course at FER, University of Zagreb.

## Implemented algorithms

- Greedy construction
- Random solution generation
- Local search
- Simulated annealing
- Tabu search

The problem is the same as in lab 1: pick a first team of 11 players and 4 substitutes under a budget, position-quota and per-club constraints, maximizing the expected points of the first team.

## Input format

A CSV file with one player per row, encoded as `cp1252`:

```text
id,position,name,club,points,price
1,GK,Player One,Club A,42.0,5.5
2,DEF,Player Two,Club B,31.0,4.5
...
```

Positions are `GK`, `DEF`, `MID` and `FW`.

## Requirements

- Python 3.8 or newer
- No external packages

## Run

```bash
python3 main.py path/to/players.csv
```

`main.py` currently runs the greedy algorithm followed by simulated annealing. Results are written to:

- `greedy_solution.txt`
- `simulated_annealing.txt`

The calls for random search, local search and tabu search are present but commented out in `main.py`; uncomment them to run those experiments. They write `random_solution.txt`, `local_optimised.txt` and `tabu_search.txt`.

## Project structure

```text
main.py                     # entry point and experiment setup
parser.py                   # CSV instance parser
models.py                   # Player and Squad models
greedy_algorithm.py
random_solution_algorithm.py
local_search_algorithm.py
Annealing.py                # simulated annealing
Tabu.py                     # tabu search
*.txt                       # example algorithm outputs
```
