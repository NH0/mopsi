import numpy as np
from basic_diffusion_cascade import propagation_step, propagation, sigma
import networkx as nx
import random_graph_construction as rg
import matplotlib.pyplot as plt


def norm_l1( vect ):
    sum = 0
    for i in range(len(vect)):
        sum += abs(vect[i])
    return sum

def PageRank(G, epsilon=10**(-4), alpha=0.50):
    n = nx.number_of_nodes(G)
    S = nx.adjacency_matrix(G, weight=None).toarray()
    S2 = np.zeros((n,n))
    for i in range(len(S)):
        sum = 0
        for j in range(len(S)):
            sum += S[i][j]
        if sum != 0: S2[i] = S[i]/sum
    M = alpha * S2 + (1-alpha) * 1/n * np.ones((n,n))
    old_influence_scores = 1/nx.number_of_nodes(G) * np.ones(n)
    influence_scores = np.dot(old_influence_scores,M)

    while (norm_l1(influence_scores - old_influence_scores) >= epsilon):
        # print("Norme L1: ", norm_l1(influence_scores - old_influence_scores))
        old_influence_scores, influence_scores = influence_scores, np.dot(influence_scores,M)

    return influence_scores

def influential_nodes_PageRank(G, nb_nodes):
    influence_scores = PageRank(G)
    influential_nodes = sorted(range(len(influence_scores)), key=lambda t: -influence_scores[t])

    return influential_nodes[:nb_nodes]

# new_graph = True # Saving a graph instead of generating a new graph each time
# if(new_graph):
#     G = rg.random_graph_from_graphon(30, rg.W_exp, WC_model=True)
#     nx.write_edgelist(G, "graph.txt")
#
# else:
#     G = nx.read_edgelist("graph.txt", nodetype=int)
#
# expected_size = []
#
# nb_influential_nodes = [n for n in range(15)]
# influential_nodes = influential_nodes_PageRank(G,15)
# print(influential_nodes)
# for nb in nb_influential_nodes: # Computation of the expected sizes of the infected set given an infection through nb initially infected nodes, with a greedy algorithm
#     expected_size.append(sigma(G, influential_nodes[:nb]))
#
# plt.figure(1)
# plt.plot(nb_influential_nodes, expected_size)
# plt.title("Number of infected nodes as a function of the initial number of infected nodes")
# plt.xlabel("Number of initially infected vertices")
# plt.ylabel("Expected size of infected vertices")
# plt.show()
