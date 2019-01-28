import networkx as nx

def findMaxNode(V):
    maxDeg = 0
    node = V[0]
    for v in V:
        if (nx.len(nx.neighbors(G,v))>maxDeg):
            maxDeg = nx.len(nx.neighbors(G,v))
            node = v
    return node

def generalizedDegreeDiscount(G,k,p):
    V = [i for i in range(nx.number_of_nodes(G))]
    S = []

    gdd = [len(nx.neighbors(G,i)) for i in range(nx.number_of_nodes(G))]
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
            dv = len(nx.neighbors(G,v))
            gdd[v] = dv - 2*t[v] - (dv - t[v])*t[v]*p + t[v]*(t[v]-1)*p/2 - sumtw*p
            if gdd[v]<0:
                gdd[v] = 0

    return S
