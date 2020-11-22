import networkx as nx
from dilemma import *
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Command: main.py [n_initial] [n_final] [step]")
        exit(0)

    n_initial = int(sys.argv[1])
    n_final = int(sys.argv[2])
    step = int(sys.argv[3])
    if n_initial < 0 or n_final < 0 or step < 0 or \
            n_initial > n_final or step > abs(n_final - n_initial):
        print("Invalid Arguments")
        exit(0)

    types = ["random", "biggest_hubs"]
    dilemmas = ['C', 'D']
    per_changes = 0.05
    iterations = 50

    for n in range(n_initial, n_final, step):
        G = gen_dilemma_uscale_graph(n)
        n_changes = int(per_changes * n)
        for d in dilemmas:
            setup(G, d)
            for t in types:
                G_cpy = G.copy(G)
                population_entropy(G_cpy, n_changes, t, d)
                simulate(G_cpy, iterations)
