import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def graph_inline(G: nx.Graph, pos: dict) -> None:
    # draw graph in inset
    coop = [node for node in G.nodes if G.nodes[node]["type"] == 'C']
    defect = [node for node in G.nodes if G.nodes[node]["type"] == 'D']
    nx.draw_networkx_nodes(G, pos, nodelist=coop,
                           node_color='g')
    nx.draw_networkx_nodes(G, pos, nodelist=defect,
                           node_color='r')
    nx.draw_networkx_edges(G, pos, alpha=0.4)


def add_degree_label(G: nx.Graph, pos: dict) -> None:
    labels = {}

    for node in G.nodes():
        labels[node] = G.degree[node]
    nx.draw_networkx_labels(G, pos, labels, font_size=16, font_color="white")


def graph_display(G: nx.Graph, options: dict) -> None:
    pos = nx.spring_layout(G, k=0.8)
    plt.figure(figsize=(18, 18))

    if options.get("inline"):
        graph_inline(G, pos)
    if options.get("node_labeled"):
        add_degree_label(G, pos)

    plt.axis("off")
    # plt.savefig("../results/GD_{}.png".format(year))
    plt.show()


def graph_save(G: nx.Graph, n: int):
    nx.write_gexf(G, "../results/graph_size{}.gexf".format(n))
