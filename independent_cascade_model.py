import networkx as nx
import matplotlib.pyplot as plt
import random_graph_construction as rg
import random as rd
# from networkx.drawing.nx_agraph import graphviz_layout

# One step in the propagation with thresholds
def propagation_step(G, some_nodes, threshold):
    new_infected_nodes = []
    for node in range(nx.number_of_nodes(G)):
        if node not in some_nodes:
            neighboring_weight = 0
            for neighbor in nx.all_neighbors(G, node):
                if neighbor in some_nodes:
                    neighboring_weight += G[neighbor][node]['weight']
            if neighboring_weight > threshold[node]:
                new_infected_nodes.append(node)
    return new_infected_nodes

# Complete propagation, with the cascade threshold model
def propagation(G, starting_nodes, threshold):
    new_infected_nodes = [0]
    infected_nodes = starting_nodes[:]
    while(len(new_infected_nodes)>0):
        new_infected_nodes = propagation_step(G, infected_nodes, threshold)
        infected_nodes += new_infected_nodes
    return infected_nodes

# Computation of the expected size sigma (which is the expectation of the number of infected nodes at the end)
def sigma(G, some_nodes, threshold):
    nb_iter = 50
    mean = 0
    for it in range(nb_iter):
        mean += len(propagation(G, some_nodes, threshold))
    mean /= nb_iter
    return mean

# Greedy algorithm for the most influential nodes
def influential_nodes(G, max_nb_nodes, threshold):
    A = []
    for i in range(max_nb_nodes):
        sigma_A = sigma(G, A, threshold)
        print(sigma_A)
        marginal_gain = 0
        for node in range(nx.number_of_nodes(G)): # Search for the node not already in A giving the best marginal gain
            if node not in A:
                B = A[:]
                B.append(node)
                sigma_B = sigma(G, B, threshold)
                if(sigma_B-sigma_A > marginal_gain):
                    marginal_gain = sigma_B-sigma_A
                    best_node = node
        A.append(best_node)
    return(A)

# Display a graph with in orange the most influential nodes, in red the nodes infected by those nodes (which is random) and in green the nodes which weren't infected
def display_graph(G, infected, influential_nodes, thresholds):
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

    # Adding labels to the edges
    edge_labels = {(n1,n2): G[n1][n2]['weight'] for (n1,n2) in G.edges()}

    # # Position for the nodes of the graph
    # pos = graphviz_layout(G)

    # Print the different thresholds for each node
    for i in range(nx.number_of_nodes(G)):
        print(i, ": ", thresholds[i])

    # Plot of the graph
    nx.draw_networkx(G, node_color=node_colors)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)


## Tests for different graphs
number_of_nodes = 10
number_of_influential_nodes = 2
bernoulli_mean = 1/3
G, thresholds = rg.random_graph_with_random_weights(number_of_nodes, bernoulli_mean, 1)

influential_nodes = influential_nodes(G, number_of_influential_nodes, thresholds)
print(influential_nodes)
infected = propagation(G, influential_nodes, thresholds) # Listof infected nodes after the propagation

influential_nodes2 = rd.sample([k for k in range(number_of_nodes)], number_of_influential_nodes)
infected2 = propagation(G, influential_nodes2, thresholds)

plt.figure(1)
plt.subplot(1,2,1)
display_graph(G, infected, influential_nodes, thresholds)
plt.text(-0.2, 1.0, "Number of infected nodes: "+str(len(infected)))
plt.text(-0.2, 1.1, "Expected size: "+str(sigma(G, influential_nodes, thresholds)))
plt.title("Diffusion with influential nodes obtained with the greedy algorithm")

plt.subplot(1,2,2)
display_graph(G, infected2, influential_nodes2, thresholds)
plt.text(-0.2, 1.0, "Number of infected nodes: "+str(len(infected2)))
plt.text(-0.2, 1.1, "Expected size: "+str(sigma(G, influential_nodes2, thresholds)))
plt.title("Diffusion with random influential nodes")

plt.show()
