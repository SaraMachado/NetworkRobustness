import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


class ResTable:
    def __init__(self):
        self.data = []
        self.columns = ['# Defectors',
                        '# Cooperators',
                        '% Defector',
                        '% Cooperators',
                        'Avg Fit Level',
                        'Max Fit Level']
        self.rows = []

    def add_line(self, G: nx.Graph, iteration: int):
        # [#Defectors, #Cooperators, %Defectors, %Cooperators, Avg Fit, Max Fit]
        new_line = [0] * len(self.columns)

        for node in G.nodes():
            if G.nodes[node]["fit"] > new_line[-1]:
                new_line[-1] = G.nodes[node]["fit"]
            new_line[-2] += G.nodes[node]["fit"]

            if G.nodes[node]["type"] == 'D':
                new_line[0] += 1
            else:
                new_line[1] += 1

        new_line[2] = new_line[0] / G.number_of_nodes()
        new_line[3] = new_line[1] / G.number_of_nodes()

        self.rows.append("Iteration: {}".format(iteration))
        self.data.append(new_line)

    def generate_table(self, title=None):
        y_offset = np.zeros(len(self.columns))
        cell_text = []
        for row in range(len(self.rows)):
            y_offset = y_offset + self.data[row]
            line = []
            for i in range(len(self.columns)):
                if i == 2 or i == 3:
                    line.append("{:.2f}%".format(y_offset[i]))
                    continue
                line.append("{}".format(y_offset[i]))
            cell_text.append(line)

        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.box(on=None)

        table = plt.table(cellText=cell_text,
                              rowLabels=self.rows,
                              colLabels=self.columns,
                              loc='center')
        table.scale(1, 1.5)
        if title is not None: plt.title(title)
        plt.show()

    def clear(self):
        self.data.clear()
        self.rows.clear()