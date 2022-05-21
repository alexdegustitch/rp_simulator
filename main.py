import networkx as nx
import matplotlib.pyplot as plt
import utils

N = int(input())
M = int(input())
G = utils.graph(N, M)
nx.draw_circular(G, with_labels=True)
plt.show()
