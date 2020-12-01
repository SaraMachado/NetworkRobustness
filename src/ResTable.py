import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import csv


class ResTable:
    def __init__(self):
        self.data = []
        self.columns = ['# Defectors',
                        '# Cooperators',
                        '% Defectors',
                        '% Cooperators',
                        'Avg Fit Level',
                        'Max Fit Level']
        self.rows = []
        with open("../results/output.csv", "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["graph_name", "percentage"])

    def add_line(self, G: nx.Graph, per_changes: float) -> int:
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

        new_line[-2] /= G.number_of_nodes()
        new_line[2] = new_line[0] / G.number_of_nodes() * 100
        new_line[3] = new_line[1] / G.number_of_nodes() * 100

        self.rows.append("% Changes: {}".format(per_changes))
        self.data.append(new_line)
        return (new_line[1], new_line[0])[new_line[0] < new_line[1]]

    def generate_table(self, title=None):
        cell_text = []
        for row in range(len(self.rows)):
            y_offset = np.zeros(len(self.columns))
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
        plt.savefig("../results/test.png")

    def save(self, filename: str):
        # filename: size + dilemma: D|C + strategy: R|H
        with open('../results/output.csv', 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([filename, len(self.rows)*0.01])

    def save_baseline(self, filename: str):
        with open('../results/baseline/{}.csv'.format(filename), 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(["Defectors", "Cooperators", "%Defectors",
                                 "%Cooperators", "Avg Fit", "Max Fit"])
            csv_writer.writerows(self.data)

    def clear(self):
        self.data.clear()
        self.rows.clear()
