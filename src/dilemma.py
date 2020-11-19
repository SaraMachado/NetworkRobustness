from display import *
import networkx as nx


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


def update_node_type(G: nx.Graph, node: int, node_type: str, fit: float) -> None:
    # TODO
    pass


def simulate(G: nx.Graph, iterations: int, step: int = 1) -> None:
    for i in range(0, iterations, step):
        for node in G.nodes():
            fit = G.nodes[node]["fit"] * i + node_fitness(G, node)
            update_node_type(G, node, G.nodes[node]["type"], fit)
    graph_display(G, {"inline": True, "node_labeled": True})


""" 
Falta as funcoes todas dos resultados que queremos arranjar;
Falta como  dar o update segundo a influência;
Falta possiveis funcoes de parse e storage de imagens e resultados.
"""