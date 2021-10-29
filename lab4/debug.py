import networkx as nx
graph = [[1],[2,3],[4,5],[4,6],[5,6,8],[7],[8,10],[9,11],[9,],[11],[11]]

G = nx.DiGraph()
for i in range(len(graph)):
    adges = [(i,to,-1) for to in graph[i]]
    G.add_weighted_edges_from(adges)

nx.draw_planar(G,with_labels = True)


[print(n) for n in G.successors(5)]

def find_longest_path(graph,_from,_to):
    vertexes_to_check = [_from,]
    F = dict()
    F[_from] = (0,[])
    current_layer = {_from,}
    while len(current_layer) != 0:
        neighbors = list()
        for vertex in current_layer:
            for neighbor in graph.successors(vertex):
                neighbors.append(neighbor)
        next_layer_set = set(neighbors)
        for neighbor in next_layer_set:
            F[neighbor] = (0,[])
            for source in current_layer:
                if nx.has_path(graph,source,neighbor):
                    path = nx.shortest_path(graph,source,neighbor)
                    if F[neighbor][0] < (len(path) + F[source][0]):
                        F[neighbor] = (len(path) - 1 + F[source][0] , path)
        current_layer = next_layer_set
    return F

print(find_longest_path(G,0,11))
