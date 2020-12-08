# Network Science - Project 2020/2021

The project runs a robustness analysis of a scale-free network in the Prisoner's Dilemma environment, on graphs of a given size. The way this is performed is by, for each graph size, initially generating a scale-free network using the Barabási-Albert Model. Then it is assigned to be a cooperator graph and a progressively larger defector intrusion is simulated until the network is overthrown. Afterwards, the roles are reversed and the test is performed for a defector network. For each graph size, this is executed twice, once for each type of intrusion (Random or Hubs). 

In order to run this analysis:
* Enter the `src` folder
* Run the file `main.py [nodes_initial] [nodes_final] [step] [version]`

The files of analysis will be saved to the folder `results`. The filenames of the saved files will have the following format:
* `output.csv`, Contains all the robustness percentages for a specific graph size, strategy and network type.
* `[size][C|D][R|H].csv`, Data of the evolution of the network of the specified [size]. The C or D represents the type of network, cooperator or defector, respectively, and the R or H the strategy applied for the exchange of nodes, Random or Hubs strategy.
* `RA_[version].png`, Graph on the general analysis containing the four possible combinations between the network type and the method used to exchange the nodes as mentioned previously.


---

#### Developed By

| Name | University | Identifier | Email |
| ---- | ---- | ---- | ---- |
| Sara Machado | Instituto Superior Técnico | 86923 | sara.f.machado@tecnico.ulisboa.pt |
| João Galamba | Instituto Superior Técnico | 90735 | joao.catarino.g@tecnico.ulisboa.pt |
| Manuel Mascarenhas | Instituto Superior Técnico | 90751 | manuel.d.mascarenhas@tecnico.ulisboa.pt |

