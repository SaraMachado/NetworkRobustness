import csv
import os

from display import *
import networkx as nx
import ResTable
import random
from matplotlib.legend_handler import HandlerLine2D


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
    return nx.scale_free_graph(nodes).to_undirected()


def setup(G: nx.Graph, dilemma: str):
    for node in G.nodes():
        G.nodes[node]["type"] = dilemma
        G.nodes[node]["fit"] = 0


def update_node_type(G: nx.Graph, node: int) -> None:
    neighbour = random.choice(list(G[node]))
    if G.nodes[neighbour]["fit"] > G.nodes[node]["fit"]:
        G.nodes[node]["type"] = G.nodes[neighbour]["type"]


def simulate(G: nx.Graph, iterations: int, dilemma: str) -> bool:
    for i in range(iterations):
        for node in G.nodes():
            fit = G.nodes[node]["fit"] * i + node_fitness(G, node)
            G.nodes[node]["fit"] = fit / (i + 1)
        for node in G.nodes():
            update_node_type(G, node)

        if is_changed(G, dilemma): return True
    return False
    # graph_display(G, {"inline": True, "node_labeled": True})
    # figure out when to save image lmao


def is_changed(G: nx.Graph, dilemma: str) -> bool:
    for node in G.nodes():
        if G.nodes[node]["fit"] == dilemma: return False
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
    # TODO add all strategies if more
    if strategy == "random":
        random_entropy(G, changes, dilemma)
    elif strategy == "biggest_hubs":
        biggest_hubs_entropy(G, changes, dilemma)
    """ Maybe with degree distribution ???? lmao"""


def generate_results() -> dict:
    # filename: size + dilemma: D|C + strategy: R|H + .csv
    results = {}
    with open('../results/output.csv', 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            size = row["graph_name"][:-2]
            types = row["graph_name"][-2:]
            results[size][types] = row["percentage"]
    return results


def robustness_analysis(results: dict, version: str = "") -> None:
    """{1000: {'CR': float, 'CH': float, 'DR': float, 'DH': float},...}"""
    rob_cop_ran, rob_cop_hub, rob_def_ran, rob_def_hub, = [], [], [], []

    for size in results.keys():
        rob_cop_ran.append(results.get(size)['CR'])
        rob_cop_hub.append(results.get(size)['CH'])
        rob_def_ran.append(results.get(size)['DR'])
        rob_def_hub.append(results.get(size)['DH'])

    line1, = plt.plot(list(results.keys()), rob_cop_ran, label="Percentage Cooperators Random Strategy")
    plt.plot(list(results.keys()), rob_cop_hub, label="Percentage Cooperators Biggest Hubs Strategy")
    plt.plot(list(results.keys()), rob_def_ran, label="Percentage Defectors Random Strategy")
    plt.plot(list(results.keys()), rob_def_hub, label="Percentage Defectors Biggest Hubs Strategy")

    plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
    plt.yticks(np.arange(0, 1, 0.5))
    plt.savefig("../results/RA{}.png".format(version))
    plt.show()


""" 
Falta as funcoes todas dos resultados que queremos arranjar;
Falta possiveis funcoes de parse e storage de imagens e resultados.
Alterar display.py para colorir os nos de acordo com cenas que queiramos
"""
