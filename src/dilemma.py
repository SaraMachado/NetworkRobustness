import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
from math import exp
from matplotlib.legend_handler import HandlerLine2D
from display import *


def game(player_type: str, opponent_type: str) -> float:
    if player_type == 'C' and opponent_type == 'C':
        return 1
    elif player_type == 'C' and opponent_type == 'D':
        return -0.2
    elif player_type == 'D' and opponent_type == 'C':
        return 1.2
    return 0


def node_fitness(G: nx.Graph, node_id: int) -> float:
    fit = 0
    for neighbour in G[node_id]:
        fit += game(
            G.nodes[node_id]["type"],
            G.nodes[neighbour]["type"]
        )
    return fit / len(G[node_id])


def gen_dilemma_uscale_graph(nodes: int) -> nx.Graph:
    return nx.barabasi_albert_graph(nodes, 4)


def setup(G: nx.Graph, dilemma: str) -> None:
    for node in G.nodes():
        G.nodes[node]["type"] = dilemma
        G.nodes[node]["fit"] = 0


def probability_change(neighbour_fit: float, node_fit: float) -> bool:
    beta = 10
    p = pow(1 + pow(exp(1), - beta * (neighbour_fit-node_fit)), -1)
    return random.random() <= p


def update_nodes_type(G: nx.Graph) -> None:
    to_change = []
    for node in G.nodes():
        neighbour = random.choice(list(G[node]))

        if G.nodes[node]["type"] == G.nodes[neighbour]["type"]: continue

        if probability_change(G.nodes[neighbour]["fit"], G.nodes[node]["fit"]):
            to_change.append(node)

    for node in to_change:
        G.nodes[node]["type"] = ('C', 'D')[G.nodes[node]["type"] == 'C']


def simulate(G: nx.Graph, generations: int, dilemma: str) -> bool:
    for i in range(generations):
        # graph_display(G, {"inline": True, "node_labeled": True})
        for node in G.nodes():
            fit = G.nodes[node]["fit"] * i + node_fitness(G, node)
            G.nodes[node]["fit"] = fit / (i + 1)
        update_nodes_type(G)

        if is_changed(G, dilemma): return True
    return False


def is_changed(G: nx.Graph, dilemma: str) -> bool:
    for node in G.nodes():
        if G.nodes[node]["type"] == dilemma:
            return False
    return True


def random_entropy(G: nx.Graph, changes: int, dilemma: str) -> None:
    nodes = random.choices(list(G.nodes), k=changes)
    for i in nodes:
        G.nodes[i]["type"] = ('C', 'D')[dilemma == 'C']


def biggest_hubs_entropy(G: nx.Graph, changes: int, dilemma: str) -> None:
    degrees = sorted([(n, d) for n, d in G.degree()], key=lambda pair: pair[1], reverse=True)

    for n, _ in degrees[:changes]:
        G.nodes[n]["type"] = ('C', 'D')[dilemma == 'C']


def population_entropy(G: nx.Graph, changes: int, strategy: str, dilemma: str) -> None:
    if strategy == "random":
        random_entropy(G, changes, dilemma)
    elif strategy == "biggest_hubs":
        biggest_hubs_entropy(G, changes, dilemma)


def generate_results() -> dict:
    # filename: size + dilemma: D|C + strategy: R|H + .csv
    results = {}
    with open('../results/output.csv', 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            size = row["graph_name"][:-2]
            types = row["graph_name"][-2:]
            if size not in results.keys():
                results[size] = {}
            results[size][types] = row["percentage"]
    return results


def robustness_analysis(results: dict, version: str = "") -> None:
    # {1000: {'CR': float, 'CH': float, 'DR': float, 'DH': float},...}
    rob_cop_ran, rob_cop_hub, rob_def_ran, rob_def_hub, = [], [], [], []

    for size in results.keys():
        rob_cop_ran.append(float(results.get(size)['CR']))
        rob_cop_hub.append(float(results.get(size)['CH']))
        rob_def_ran.append(float(results.get(size)['DR']))
        rob_def_hub.append(float(results.get(size)['DH']))

    keys = [float(i) for i in list(results.keys())]
    line1, = plt.plot(keys, rob_cop_ran, label="Percentage Cooperators Random Strategy")
    plt.plot(keys, rob_cop_hub, label="Percentage Cooperators Biggest Hubs Strategy")
    plt.plot(keys, rob_def_ran, label="Percentage Defectors Random Strategy")
    plt.plot(keys, rob_def_hub, label="Percentage Defectors Biggest Hubs Strategy")

    plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.savefig("../results/RA_{}.png".format(version))
    plt.show()
