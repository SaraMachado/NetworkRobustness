import networkx as nx
import ResTable as rt
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

    res_table = rt.ResTable()
    types = ["random", "biggest_hubs"]
    dilemmas = ['C', 'D']
    iterations = 50

    per_changes = 0
    is_changed = False
    for n in range(n_initial, n_final, step):
        G = gen_dilemma_uscale_graph(n)
        for d in dilemmas:
            setup(G, d)
            for t in types:
                while not is_changed and per_changes < 1:
                    per_changes += 0.01
                    G_cpy = G.copy(G)
                    population_entropy(G_cpy, int(per_changes * n), t, d)
                    is_changed = simulate(G_cpy, iterations, d)
                    res_table.add_line(G, per_changes)
                # res_table.generate_table()
                res_table.save("{}{}{}".format(n, d, ('H', 'R')[t[0].upper() == 'R']))
                per_changes = 0
                is_changed = False
