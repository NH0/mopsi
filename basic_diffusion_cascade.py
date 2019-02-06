import networkx as nx
import pylab
import random as rd
import random_graph_construction as rg
import matplotlib.pyplot as plt
import numpy as np
# from sets import Set


wt = 1/10

# One step of a random propagation given a fixed set of nodes infected at the start. Returns the new infected nodes
def propagation_step(G, is_infected_node, infectious_nodes):
    new_infected_nodes = []
    for node in infectious_nodes:
        for neighbor in G.successors(node):
            if not is_infected_node[neighbor]: # If not already infected
                # print(G[node][neighbor]['weight'])
                if rd.random()<G[node][neighbor]['weight']:
                    new_infected_nodes.append(neighbor)
                    is_infected_node[neighbor] = True
    return new_infected_nodes

# Complete propagation, with each node trying to infect another node
def propagation(G, starting_nodes):
    new_infected_nodes = starting_nodes[:]
    infected_nodes = starting_nodes[:]
    is_infected_node = [False for i in range(G.number_of_nodes())]
    for node in starting_nodes:
        is_infected_node[node] = True
    while(len(new_infected_nodes)>0):
        new_infected_nodes = propagation_step(G, is_infected_node, new_infected_nodes)
        infected_nodes += new_infected_nodes
    return infected_nodes

# Computation of the expected size sigma (which is the expectation of the number of infected nodes at the end)
def sigma(G, some_nodes, nb_iter=120):
    mean = 0
    for it in range(nb_iter):
        mean += len(propagation(G, some_nodes))
    mean /= nb_iter
    return mean

# Greedy algorithm for the most influential nodes
def influential_nodes(G, max_nb_nodes):
    A = []
    for i in range(max_nb_nodes):
        sigma_A = sigma(G, A)
        marginal_gain = 0
        for node in nx.nodes(G): # Search for the node not already in A giving the best marginal gain
            if node not in A:
                B = A[:]
                B.append(node)
                sigma_B = sigma(G, B)
                if(sigma_B-sigma_A > marginal_gain):
                    marginal_gain = sigma_B-sigma_A
                    best_node = node
        A.append(best_node)
    return A

# Display a graph with in orange the most influential nodes, in red the nodes infected by those nodes (which is random) and in green the nodes which weren't infected
def display_graph(G, infected, influential_nodes):
    nb_nodes = nx.number_of_nodes(G)

    # Graphic settings
    node_colors = ['g' for k in range(nb_nodes)]

    # Coloring in red the infected nodes
    for node in range(nb_nodes):
        if node in infected:
            node_colors[node] = 'r'

    # Coloring in orange the most influential nodes
    for node in range(nb_nodes):
        if node in influential_nodes:
            node_colors[node] = 'orange'

    # Plot of the graph
    nx.draw_networkx(G, node_color=node_colors)

# Parsing function for the graph data set
def read_data(filename, in_degree_model, split, first_row):
    G = nx.Graph()
    nodes = set()
    edges = []

    file = open(filename,'r')
    rows = [row.rstrip('\n') for row in file]
    rows = rows[first_row:]

    for row in rows:
        column = row.split(split)
        for node in column:
            nodes.add(int(node))

    if(in_degree_model):
        weight_per_node = [0 for node in range(max(nodes)+1)]
        for row in rows:
            column = row.split(split)
            weight_per_node[int(column[1])] += 1

        for k in range(len(weight_per_node)):
            if weight_per_node[k] != 0:
                weight_per_node[k] = 1/weight_per_node[k]

    else:
        weight = [0.1, 0.01, 0.001]
        weight_per_node = [rd.choice(weight) for node in range(max(nodes)+1)]

    for row in rows:
        column = row.split(split)
        edges.append((int(column[0]),int(column[1]),weight_per_node[int(column[1])]))

    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)

    print("Number of nodes: ", nx.number_of_nodes(G))
    print("Number of edges: ", nx.number_of_edges(G))
    return G

# Confidence interval for the computation of sigma
def h(x):
    return (1+x)*np.log(1+x)-x

def confidence_interval(gamma, sigma, M=120, nb_nodes):
    lower_bound = sigma/(1+gamma)
    upper_bound = sigma/(1-gamma)
    probability = 1 - 2 * np.exp(-M*h(gamma/nb_nodes))
    return lower_bound, upper_bound, probability
