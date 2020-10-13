import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from math import ceil
from collections import Counter
from numpy.random import choice

np.random.seed(512)

n_V = 8192       # given number of vertices
lambd = 1.25
E = 1            # initial number of edges

# empty network creation
G = nx.Graph()

# adding two vertices with edge between
G.add_edge(1, 2)

for V in range(3, n_V+1):
    
    deltaE = ceil(lambd*E/(G.number_of_nodes()-1))
    deltaE = 1
    
    # dict of vertex joining probabilities
    probs = [d/(2*E) for n, d in nx.degree(G)]
    
    # choice of a vertex to join
    verts_to_join = choice([i+1 for i in range(V-1)],
                           deltaE, replace=False,
                           p=probs)
    
    # adding new vertex
    G.add_node(V)
    
    # adding edges to choosen vertices
    for v in verts_to_join:
        G.add_edge(V, v)
        
    E += deltaE

# network drawing
#nx.draw(G, with_labels=True)

freq_seq = sorted([d for n, d in nx.degree(G)], reverse=True)
degreeCount = Counter(freq_seq)
d, f = zip(*degreeCount.items())

# slope and intercept estimation
slope, intercept = np.polyfit(np.log(d), np.log(f), 1)
#slope = -3
print(slope, intercept)

# plots drawing
plt.figure(figsize=(7,9))

# frequency distribution subplot
plt.subplot(211)
plt.loglog(d, f,
           linestyle='None',
           marker='+',
           markersize=3)

# drawing approximation line
plt.loglog(d, np.e**intercept*np.array(d)**slope, c='darkgreen')

plt.xlabel('Degree')
plt.ylabel('Frequency')

# rank distribution subplot
plt.subplot(212)
plt.loglog([i+1 for i in range(len(d))], d, linewidth=0.3,
           marker='+',
           markersize=3)
plt.xlabel('Rank')
plt.ylabel('Degree')


    