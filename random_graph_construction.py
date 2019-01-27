import networkx as nx
import random as rd
import pylab

# Random generation of an Erdos Reniy graph with fixed size
def random_graph(nb_nodes, bernoulli_mean):
    G = nx.Graph()

    # Nodes creation
    list_nodes = [k for k in range(nb_nodes)]
    G.add_nodes_from(list_nodes)

    # Edges creation
    wt = 1/3
    list_edges = []
    for i in range(nb_nodes):
        for j in range(i+1,nb_nodes):
            if rd.random() < bernoulli_mean:
                list_edges.append((i,j,wt))
    G.add_weighted_edges_from(list_edges)

    return(G)

# Random generation of an Erdos Reniy graph with fixed size adapted for the threshold model and randomly weighted edges
def random_graph_with_random_weights(nb_nodes, bernoulli_mean, threshold_flag):
    G = nx.Graph()

    # Nodes creation
    list_nodes = [k for k in range(nb_nodes)]
    G.add_nodes_from(list_nodes)

    # Edges creation
    list_edges = []
    for i in range(nb_nodes):
        for j in range(i+1,nb_nodes):
            if rd.random() < bernoulli_mean:
                wt = rd.random()/nb_nodes # The weights are within 0 and 1/nb_nodes to ensure that at all time sum(wt_i)<=1
                list_edges.append((i,j,wt))
    G.add_weighted_edges_from(list_edges)

    if threshold_flag:
        thresholds = [rd.random() for k in range(nb_nodes)]
        return(G, thresholds)
    else:
        return(G)
