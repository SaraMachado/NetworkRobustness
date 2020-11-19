from display import *
import networkx as nx
import random


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


def gen_dilemma_uscale_graph(nodes: int, dilemma: str) -> nx.Graph:
    G = nx.scale_free_graph(nodes).to_undirected()

    for node in G.nodes():
        G.nodes[node]["type"] = dilemma
        G.nodes[node]["fit"] = 0

    return G


def update_node_type(G: nx.Graph, node: int) -> None:
    neighbour = random.choice(list(G[node]))
    if G.nodes[neighbour]["fit"] > G.nodes[node]["fit"]:
        G.nodes[node]["type"] = G.nodes[neighbour]["type"]


def simulate(G: nx.Graph, iterations: int, step: int = 1) -> None:
    for i in range(0, iterations, step):
        for node in G.nodes():
            fit = G.nodes[node]["fit"] * i + node_fitness(G, node)
            G.nodes[node]["fit"] = fit / (i + 1)
        for node in G.nodes():
            update_node_type(G, node)
    graph_display(G, {"inline": True, "node_labeled": True})


def random_entropy(G: nx.Graph, changes: int, dilemma: str) -> None:
    nodes = random.choices(list(G.nodes), k=changes)
    for i in nodes:
        G.nodes[i]["type"] = dilemma


def biggest_hubs_entropy(G: nx.Graph, changes: int, dilemma: str) -> None:
    degrees = sorted(list(set([d for _, d in G.degree()])), reverse=True)
    to_change = changes
    while to_change != 0:
        for node in G.nodes():
            if G.degree[node] == degrees[0]:
                G.nodes[node]["type"] = dilemma
                to_change -= 1
            if to_change == 0: return
        degrees.pop(0)


def population_entropy(G: nx.Graph, changes: int, strategy: str, dilemma: str) -> None:
    # TODO add all strategies if more
    if strategy == "random":
        random_entropy(G, changes, dilemma)
    elif strategy == "biggest_hubs":
        biggest_hubs_entropy(G, changes, dilemma)


""" 
Falta as funcoes todas dos resultados que queremos arranjar;
Falta possiveis funcoes de parse e storage de imagens e resultados.
"""