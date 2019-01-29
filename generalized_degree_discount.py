import networkx as nx
import random_graph_construction as rg
from basic_diffusion_cascade import sigma

n = 400
k = 4
p = 0.01

def findMaxNode(V):
    maxDeg = 0
    node = V[0]
    for v in V:
        if (G.degree[v]>maxDeg):
            maxDeg = G.degree[v]
            node = v
    return node

def generalizedDegreeDiscount(G,k,p):
    V = [i for i in range(nx.number_of_nodes(G))]
    S = []

    gdd = [G.degree[i] for i in range(nx.number_of_nodes(G))]
    t = [0]*nx.number_of_nodes(G)

    for i in range(k):
        u = findMaxNode(V)
        S.append(u)
        V.remove(u)
        NB = []

        for v in nx.neighbors(G,u):
            NB.append(v)
            t[v] += 1

            for w in nx.neighbors(G,v):
                if not(w in NB):
                    NB.append(w)

        for v in NB:
            sumtw = 0
            for w in nx.neighbors(G,v):
                if not(w in S):
                    sumtw += t[w]
            dv = G.degree[v]
            gdd[v] = dv - 2*t[v] - (dv - t[v])*t[v]*p + t[v]*(t[v]-1)*p/2 - sumtw*p
            if gdd[v]<0:
                gdd[v] = 0

    return S

G = rg.random_graph_from_graphon(n,rg.W_exp)
print("##### STARTING CALCULATIONS #####")
S = generalizedDegreeDiscount(G,k,p)
print(S)
print("##### STARTING NODES FOUND #####")
avgSize = sigma(G,S)
print("##### AVERAGE NUMBER OF INFECTED NODES FOUND #####")
print(avgSize)
