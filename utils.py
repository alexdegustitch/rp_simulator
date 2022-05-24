import math
from itertools import chain
from random import randint, random, shuffle


import networkx as nx


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

def graph_from_file(file_path = "initial_graph.txt"):
    G = nx.Graph()
    with open(file = file_path, mode = 'r') as f:
        N = int(f.readline())
        G = nx.empty_graph(N)
        for line in f:
            edge = tuple(line.split(' '))
            v1 = int(edge[0])
            v2 = int(edge[1])
            if(0 <= v1 and v1 < N and 0 <= v2 and v2 < N):
                G.add_edge(int(edge[0]), int(edge[1]))

    return G

def find_not_bridges(G, root = None):
    multigraph = G.is_multigraph()
    H = nx.Graph(G) if multigraph else G
    chains = nx.chain_decomposition(H, root=root)
    chain_edges = set(chain.from_iterable(chains))
    not_bridges = []
    for u, v in H.edges():
        if (u, v) not in chain_edges and (v, u) not in chain_edges:
            if multigraph and len(G[u][v]) > 1:
                not_bridges.append((u, v))
        else:
            not_bridges.append((u, v))
    return not_bridges

def reliability_polynomial(G, p):
    G = nx.Graph(G.copy())
    if not nx.is_connected(G):
        return 0
    
    N = G.number_of_nodes()
    M = G.number_of_edges()

    connected_subgraphs_cnt = [1]

    for k in range(1, M - N + 2):

        not_bridges = find_not_bridges(G)
      
        connected_subgraphs_cnt.append(len(not_bridges))

        edge_to_remove = not_bridges[randint(0, len(not_bridges) - 1)]
        G.remove_edge(edge_to_remove[0], edge_to_remove[1])
    
    n_i_coeficient = [0 for i in range(0, M + 1)]

    n_i_coeficient[M] = 1
    for k in range(1, M - N + 2):
        n_i_coeficient[M - k] = n_i_coeficient[M - k + 1] * connected_subgraphs_cnt[k] / k

    res = 0
    for i in range(len(n_i_coeficient)):
        num = n_i_coeficient[i] * math.pow(p, i) * math.pow(1 - p, M - i)
        res += num

    return res    

def monte_carlo_method(G, p):
    G = G.copy()
    for edge in G.edges():
        if random() >= p:
            G.remove_edge(edge[0], edge[1])
    if nx.is_connected(G):
        return 1
    else:
        return 0
