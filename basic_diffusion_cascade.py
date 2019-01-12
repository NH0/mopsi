import networkx as nx
import pylab
import random as rd
import random_graph_construction as rg
import matplotlib.pyplot as plt

# One step of a random propagation given a fixed set of nodes infected at the start. Returns the new infected nodes
def propagation_step(G, some_nodes):
    new_infected_nodes = []
    for node in some_nodes:
        for neighbor in nx.all_neighbors(G,node):
            if neighbor not in some_nodes:
                if rd.random()<wt:
                    new_infected_nodes.append(neighbor)
    return new_infected_nodes

# Complete propagation, with each node trying to infect another node
def propagation(G, starting_nodes):
    new_infected_nodes = [0]
    infected_nodes = starting_nodes[:]
    while(len(new_infected_nodes)>0):
        new_infected_nodes = propagation_step(G, infected_nodes)
        infected_nodes += new_infected_nodes
    return infected_nodes

# Computation of the expected size sigma (which is the expectation of the number of infected nodes at the end)
def sigma(G, some_nodes):
    nb_iter = 50
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
        print(sigma_A)
        marginal_gain = 0
        for node in range(nx.number_of_nodes(G)): # Search for the node not already in A giving the best marginal gain
            if node not in A:
                B = A[:]
                B.append(node)
                sigma_B = sigma(G, B)
                if(sigma_B-sigma_A > marginal_gain):
                    marginal_gain = sigma_B-sigma_A
                    best_node = node
        A.append(best_node)
    return(A)

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


## Test on different graphs

# # Creation of the graph and addition of the first nodes
# G = nx.Graph()
# list_nodes = [k for k in range(8)]
# G.add_nodes_from(list_nodes)
#
# # The weight will stay the same for every edges, 1/2
# wt = 1/3
#
# # Construction of the edges
# list_weighted_edges = [(0,1,wt),(1,2,wt),(1,4,wt),(1,6,wt),(2,3,wt),(4,5,wt),(4,6,wt),(4,7,wt),(5,7,wt)]
# G.add_weighted_edges_from(list_weighted_edges)
#
# influential_nodes = influential_nodes(G, 2)
# print(influential_nodes)
# infected = propagation(G, influential_nodes) # Listof infected nodes after the propagation

# Creation of a random Erdos Reniy graph
number_of_nodes = 50
bernoulli_mean = 1/20
G = rg.random_graph(number_of_nodes, bernoulli_mean)

wt = bernoulli_mean*2
influential_nodes = influential_nodes(G, 7)
print(influential_nodes)
infected = propagation(G, influential_nodes) # Listof infected nodes after the propagation

influential_nodes2 = rd.sample([k for k in range(number_of_nodes)], 7)
infected2 = propagation(G, influential_nodes2)

plt.figure(1)
plt.subplot(1,2,1)
display_graph(G, infected, influential_nodes)
plt.text(-0.2, 1.0, "Number of RANDOMLY infected nodes: "+str(len(infected)))
plt.text(-0.2, 1.1, "Expected size: "+str(sigma(G, influential_nodes)))
plt.title("Diffusion with influential nodes obtained with the greedy algorithm")

plt.subplot(1,2,2)
display_graph(G, infected2, influential_nodes2)
plt.text(-0.2, 1.0, "Number of RANDOMLY infected nodes: "+str(len(infected2)))
plt.text(-0.2, 1.1, "Expected size: "+str(sigma(G, influential_nodes2)))
plt.title("Diffusion with random influential nodes")

plt.show()
