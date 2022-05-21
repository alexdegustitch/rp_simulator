import networkx as nx
from random import randint
from random import shuffle

def graph(N = 4, M = -1):
    if M < 0:
        M = randint(0, N * (N - 1) / 2 - N + 1)
    elif M >= 0 and M < N - 1:
        return nx.gnm_random_graph(N, M)
    elif M > N * (N - 1) / 2:
        return nx.complete_graph(N)
    else:
        M -= (N - 1)
    edges = []
    G = nx.path_graph(N)
    for i in range(1, N - 1):
        for j in range(i + 2, N + 1):
            edges.append(i * N + j)
    shuffle(edges)
    for k in range(0, M):
        i_node = edges[k] // N
        j_node = edges[k] - i_node * N
        G.add_edge(i_node, j_node)
    return G

def reliability_polynomial(G, p):
    G = nx.Graph(G)
    if not nx.is_connected(G):
        return 0
    
    N = G.nodes
    M = G.edges

    for k in range(1, M - N + 2):
        pass