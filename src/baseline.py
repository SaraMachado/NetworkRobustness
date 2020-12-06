import dilemma
import ResTable as rt
import display
import random


if __name__ == "__main__":
    lines = []
    for i in range(100):
        G = dilemma.gen_dilemma_uscale_graph(2000)
        res_table = rt.ResTable()

        for node in G.nodes():
            choice = random.choice(['C', 'D'])
            G.nodes[node]["type"] = choice
            G.nodes[node]["fit"] = 0

        for gen in range(10000):
            # display.graph_display(G, {"inline": True, "node_labeled": True})
            coop = res_table.add_line(G, gen)

            if coop == 0:
                lines.append(gen)
                break

            for node in G.nodes():
                fit = G.nodes[node]["fit"] * gen + dilemma.node_fitness(G, node)
                G.nodes[node]["fit"] = fit / (gen + 1)
            dilemma.update_nodes_type(G)

        res_table.save_baseline("baseline_{}".format(i))
    print(lines)
    print(max(lines))
    print(sorted(lines, reverse=True))
