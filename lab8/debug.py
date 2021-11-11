import networkx as nx
import numpy as np
import copy

def basaker_gowen(c_matrix,v_matrix,v):
    flow_matrix =np.zeros(np.shape(c_matrix))
    G = nx.DiGraph()
    G.add_nodes_from(range(np.shape(c_matrix)[0]))
    for i in range(np.shape(c_matrix)[0]):
        for j,_v in enumerate(c_matrix[i]):
            if _v!=0:
                G.add_edge(i,j, weight =copy.copy(c_matrix[i][j]))
    path = nx.dijkstra_path(G,0, np.shape(c_matrix)[0] - 1)
    while len(path) != 0 and v != 0:
        for i in range(1,len(path)):
            edge = [path[i-1],path[i]]
            flow_matrix[edge[0],edge[1]] += 1
            flow_v = flow_matrix[edge[0],edge[1]]
            if flow_matrix[edge[0],edge[1]] == v_matrix[edge[0]][edge[1]]:
                G[edge[0]][edge[1]]['weight'] = 9999999
            else:
                G[edge[0]][edge[1]]['weight'] = c_matrix[edge[0]][edge[1]]
            G[edge[1]][edge[0]]['weight'] = -c_matrix[edge[1]][edge[0]]
            flow_matrix[edge[1],edge[0]] -= 1
        path = nx.dijkstra_path(G,0, np.shape(c_matrix)[0] - 1)
        v-=1
    return flow_matrix

c_matrix = [[0,1,0,1,0,0],
            [1,0,2,0,2,0],
            [0,2,0,2,0,1],
            [1,0,2,0,0,0],
            [0,2,0,0,0,2],
            [0,0,1,0,2,0]]
v_matrix = [[0,1,0,1,0,0],
            [1,0,1,0,2,0],
            [0,1,0,1,0,1],
            [1,0,1,0,0,0],
            [0,2,0,0,0,2],
            [0,0,1,0,2,0]]

v =2 

print(basaker_gowen(c_matrix,v_matrix,v))