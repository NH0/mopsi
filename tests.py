import networkx as nx
import pylab
import random as rd
import random_graph_construction as rg
import matplotlib.pyplot as plt
from basic_diffusion_cascade import *
from page_rank import influential_nodes_PageRank
from generalized_degree_discount import generalizedDegreeDiscount
import time


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
# number_of_nodes = 20
# bernoulli_mean = 1/7
# G = rg.random_graph(number_of_nodes, bernoulli_mean)
#
# wt = bernoulli_mean*2
# influential_nodes = influential_nodes(G, 3)
# print(influential_nodes)
# infected = propagation(G, influential_nodes) # Listof infected nodes after the propagation
#
# influential_nodes2 = rd.sample([k for k in range(number_of_nodes)], 7)
# infected2 = propagation(G, influential_nodes2)
#
# plt.figure(1)
# plt.subplot(1,2,1)
# display_graph(G, infected, influential_nodes)
# # plt.text(0.05, 0.95, "Number of RANDOMLY infected nodes: "+str(len(infected)), transform=plt.transAxes)
# # plt.text(0.05, 0.95, "Expected size: "+str(sigma(G, influential_nodes)), transform=plt.transAxes)
# plt.title("Diffusion with influential nodes obtained with the greedy algorithm")
#
# plt.subplot(1,2,2)
# display_graph(G, infected2, influential_nodes2)
# # plt.text(0.05, 0.95, "Number of RANDOMLY infected nodes: "+str(len(infected2)), transform=plt.transAxes)
# # plt.text(0.05, 0.95, "Expected size: "+str(sigma(G, influential_nodes2)), transform=plt.transAxes)
# plt.title("Diffusion with random influential nodes")
#
# plt.show()

############## Test on a "who-trust-who" graph ##############
# G = read_data('soc-hamsterster.edges', in_degree_model=True, split=' ', first_row=2)
# nb_nodes = nx.number_of_nodes(G)

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
time0 = time.time()
timeSave = time.strftime("%d-%Hh%Mm%Ss")
############# Test on a graphon generated graph ############
new_graph = False # Saving a graph instead of generating a new graph each time
nb_nodes = 70
if(new_graph):
    G = rg.random_graph_from_graphon(nb_nodes, rg.W_exp, WC_model=True)
    nx.write_edgelist(G, "graph"+timeSave+".txt")
else:
    G = nx.read_edgelist("graph.txt", nodetype=int, create_using=nx.DiGraph)
    nb_nodes = nx.number_of_nodes(G)

# new_graph = True # Saving a graph instead of generating a new graph each time
# if(new_graph):
#     G = rg.complete_graph(WC_model=True)
#     nx.write_edgelist(G, "graph.txt")
# else:
#     G = nx.read_edgelist("graph.txt", nodetype=int)
# nb_nodes = nx.number_of_nodes(G)

# influential_nodes = influential_nodes(G,2)
# print('The two most influential nodes: ', influential_nodes)
# print('Expected size with those influential nodes: ', sigma(G, influential_nodes))

max_influentials = 20
gamma = 0.01
expected_size = []
iter = 1

nb_influential_nodes = [n for n in range(max_influentials)]

expected_size = []
upper_bound_greedy = []
lower_bound_greedy = []
print("Calculating influential nodes Greedy")
influential_nodes = influential_nodes(G,max_influentials)
print("Done\n")
for nb in nb_influential_nodes: # Computation of the expected sizes of the infected set given an infection through nb initially infected nodes, with a greedy algorithm
    # print("Node :"+str(nb+1))
    sigma1 = sigma(G, influential_nodes[:nb])
    expected_size.append(sigma1)
    lbg, ubg = confidence_interval(gamma, sigma1, nb_nodes=nb_nodes)
    upper_bound_greedy.append(ubg)
    lower_bound_greedy.append(lbg)

upper_bound_PageRank = []
lower_bound_PageRank = []
expected_size_PageRank = []
print("Calculating influential nodes Page rank")
influential_nodes_PageRank = influential_nodes_PageRank(G,max_influentials)
print("Done\n")
for nb in nb_influential_nodes: # Computation of the expected sizes of the infected set given an infection through nb initially infected nodes, with a PageRank algorithm
    sigma1 = sigma(G, influential_nodes_PageRank[:nb])
    expected_size_PageRank.append(sigma1)
    lbg, ubg = confidence_interval(gamma, sigma1, nb_nodes=nb_nodes)
    upper_bound_PageRank.append(ubg)
    lower_bound_PageRank.append(lbg)

# expected_size_degreeDiscount = []
# upper_bound_degreeDiscount = []
# lower_bound_degreeDiscount = []
# print("Calculating influential nodes generalized Degree Discount")
# influential_nodes_degreeDiscount = generalizedDegreeDiscount(G,max_influentials,p=0.01)
# print("Done")
# for nb in nb_influential_nodes: # Computation of the expected sizes of the infected set given an infection through nb initially infected nodes, with a degree discount algorithm
#     sigma1 = sigma(G, influential_nodes_degreeDiscount[:nb])
#     expected_size_degreeDiscount.append(sigma1)
#     lbg, ubg = confidence_interval(gamma, sigma1, nb_nodes=nb_nodes)
#     upper_bound_degreeDiscount.append(ubg)
#     lower_bound_degreeDiscount.append(lbg)

expected_size_random = []
upper_bound_random = []
lower_bound_random = []
print("Calculating influential nodes random")
influential_nodes_random = rd.sample([k for k in range(nx.number_of_nodes(G))],max_influentials)
print("Done\n")
for nb in nb_influential_nodes: # Computation of the expected sizes of the infected set given an infection through nb initially infected nodes, with a random list of starting nodes
    sigma1 = sigma(G, influential_nodes_random[:nb])
    expected_size_random.append(sigma1)
    lbg, ubg = confidence_interval(gamma, sigma1, nb_nodes=nb_nodes)
    upper_bound_random.append(ubg)
    lower_bound_random.append(lbg)

# print("For greedy algorithm: ", influential_nodes)
# print("For PageRank algorithm: ", influential_nodes_PageRank)
# print("For random: ", influential_nodes_random)
# print(probability(gamma, nb_nodes))

time1 = time.time()
print("Processing time "+time.strftime("%Mm%Ss",time.localtime(time1-time0)))
print('\n\a')

plt.figure(1)
plt.plot(nb_influential_nodes, expected_size, color='r',  label="Greedy Algorithm")
plt.plot(nb_influential_nodes, expected_size_PageRank, color='g', label="PageRank")
plt.plot(nb_influential_nodes, expected_size_random, color='b', label="Random")
# plt.plot(nb_influential_nodes, expected_size_degreeDiscount, color='y', label="DegreeDiscount")
# plt.errorbar(nb_influential_nodes, expected_size, yerr=[lower_bound_greedy, upper_bound_greedy], color='r',  label="Greedy Algorithm")
# plt.errorbar(nb_influential_nodes, expected_size_PageRank, yerr=[lower_bound_PageRank, upper_bound_PageRank], color='g', label="PageRank")
# plt.errorbar(nb_influential_nodes, expected_size_random, yerr=[lower_bound_random, upper_bound_random], color='b', label="Random")
# plt.errorbar(nb_influential_nodes, expected_size_degreeDiscount, yerr=[lower_bound_degreeDiscount, upper_bound_degreeDiscount], color='y', label="DegreeDiscount")
plt.title("Number of infected nodes as a function of the initial number of infected nodes")
plt.xlabel("Number of initially infected vertices")
plt.ylabel("Expected size of infected vertices")
plt.legend()
plt.show()

# file = open("data.txt", "a")
# for k in range(max_influentials):
#     file.write(str(expected_size_PageRank[k])+" ")
# file.write('\n')
# for k in range(max_influentials):
#     file.write(str(influential_nodes_PageRank[k])+" ")
# file.write('\n')
# # for k in range(max_influentials):
# #     file.write(str(expected_size_degreeDiscount[k])+" ")
# # file.write('\n')
# # for k in range(max_influentials):
# #     file.write(str(influential_nodes_degreeDiscount[k])+" ")
# # file.write('\n')
# for k in range(max_influentials):
#     file.write(str(expected_size_random[k])+" ")
# file.write('\n')
# for k in range(max_influentials):
#     file.write(str(influential_nodes_random[k])+" ")
# file.close()
# print(upper_bound_greedy)

with open("saves"+timeSave+".txt","w") as saves:
    saves.write("Expected size :")
    saves.write(str(expected_size))
    saves.write('\n\n     #####      \n\n')
    saves.write("Lower bound of greedy algorithm :")
    saves.write(str(lower_bound_greedy))
    saves.write('\n\n')
    saves.write("Lower bound of greedy algorithm :")
    saves.write(str(upper_bound_greedy))
    saves.write('\n\n     #####\n\n')
    saves.write("Influential nodes :")
    saves.write(str(influential_nodes))
