import networkx as nx
import random as rd
import pylab
import numpy as np

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

    return G

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
        return G, thresholds
    else:
        return G

def random_graph_from_graphon(nb_nodes, W, WC_model=False):
    G = nx.DiGraph()

    # Nodes creation
    list_nodes = [k for k in range(nb_nodes)]
    G.add_nodes_from(list_nodes)

    # Edges creation
    list_edges = []
    node_proba = [rd.random() for i in range(nb_nodes)]

    if(WC_model): # WC model
        list_edges_non_weighted = [[] for k in range(nb_nodes)]
        for node_i in range(nb_nodes):
            for node_j in range(node_i+1, nb_nodes):
                if rd.random() < W(node_proba[node_i], node_proba[node_j]): # We create an edge with a probability given by the graphon
                    list_edges_non_weighted[node_i].append(node_j) # Undirected graph
                    list_edges_non_weighted[node_j].append(node_i)
        for node_i in range(nb_nodes):
            if len(list_edges_non_weighted[node_i]) != 0:
                for node_j in list_edges_non_weighted[node_i]:
                    list_edges.append((node_i,node_j,1/len(list_edges_non_weighted[node_j])))
                    list_edges.append((node_j,node_i,1/len(list_edges_non_weighted[node_i])))

    else: # Trivalency model, where the probability is chosen in the set {0.1,0.01,0.001}
        for node_i in range(nb_nodes):
            for node_j in range(node_i+1, nb_nodes):
                if rd.random() < W(node_proba[node_i], node_proba[node_j]): # We create an edge with a probability given by the graphon
                    list_edges.append((node_i,node_j,rd.choice([0.1,0.01,0.001])))
                    list_edges.append((node_j,node_i,rd.choice([0.1,0.01,0.001])))

    G.add_weighted_edges_from(list_edges)

    return G

## Some usual graphons
def W_min(x,y):
    return min(x,y)

def W_exp(x,y):
    return np.exp(x+y)/(1+np.exp(x+y))
