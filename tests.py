import networkx as nx
import pylab
import random as rd
import random_graph_construction as rg
import matplotlib.pyplot as plt
from basic_diffusion_cascade import *


## Test on different graphs

############## Creation of a simple graph ################
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

############ Test on a random Erdos Reniy graph ###################
# number_of_nodes = 50
# bernoulli_mean = 1/20
# G = rg.random_graph(number_of_nodes, bernoulli_mean)
#
# wt = bernoulli_mean*2
# influential_nodes = influential_nodes(G, 7)
# print(influential_nodes)
# infected = propagation(G, influential_nodes) # Listof infected nodes after the propagation
#
# influential_nodes2 = rd.sample([k for k in range(number_of_nodes)], 7)
# infected2 = propagation(G, influential_nodes2)
#
# plt.figure(1)
# plt.subplot(1,2,1)
# display_graph(G, infected, influential_nodes)
# plt.text(-0.2, 1.0, "Number of RANDOMLY infected nodes: "+str(len(infected)))
# plt.text(-0.2, 1.1, "Expected size: "+str(sigma(G, influential_nodes)))
# plt.title("Diffusion with influential nodes obtained with the greedy algorithm")
#
# plt.subplot(1,2,2)
# display_graph(G, infected2, influential_nodes2)
# plt.text(-0.2, 1.0, "Number of RANDOMLY infected nodes: "+str(len(infected2)))
# plt.text(-0.2, 1.1, "Expected size: "+str(sigma(G, influential_nodes2)))
# plt.title("Diffusion with random influential nodes")
#
# plt.show()

############## Test on a "who-trust-who" graph ##############
# G = read_data('soc-hamsterster.edges', in_degree_model=True, split=' ', first_row=2)

# influential_nodes = influential_nodes(G,2)
# print(sigma(G, rd.sample(nx.nodes(G),3)))
# print(sigma(G, influential_nodes))
# for nb_influential_nodes in range(30):
#     influential_nodes = influential_nodes(G,nb_influential_nodes)
#     expected_size.append(sigma(G, influential_nodes))
#
# plt.figure()
# plt.plot([nb_nodes for nb_nodes in range(30)], expected_size)
# plt.show()

############# Test on a graphon generated graph ############
new_graph = False
if(new_graph):
    G = rg.random_graph_from_graphon(40, rg.W_exp)
    nx.write_edgelist(G, 'graph.txt')
else:
    G = nx.read_edgelist('graph.txt')

# influential_nodes = influential_nodes(G,2)
# print('The two most influential nodes: ', influential_nodes)
# print('Expected size with those influential nodes: ', sigma(G, influential_nodes))

expected_size = []

nb_influential_nodes = [n for n in range(20)]
for nb in nb_influential_nodes:
    expected_size.append(sigma(G, influential_nodes(G,nb)))

plt.figure(1)
plt.plot(nb_influential_nodes, expected_size)
plt.show()
