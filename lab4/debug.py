import networkx as nx
graph = [[1,5],[2,3],[4,8,5],[4,5],[8],[6,8,9],[7],[8],[9],[10]]

G = nx.DiGraph()
for i in range(len(graph)):
    adges = [(i,to,-1) for to in graph[i]]
    G.add_weighted_edges_from(adges)

nx.draw_planar(G,with_labels = True)

def find_longest_path(graph,_from,_to):
    checked_vertexes = set()
    vertexes_to_check = [_from,]
    F = dict()
    F[_from] = (0,[])
    while len(vertexes_to_check) != 0:
        vertex_to_check = vertexes_to_check.pop()
        neighbors = graph.successors(vertex_to_check)
        for neighbor in neighbors:
            if neighbor in checked_vertexes:
                continue
            path = nx.shortest_path(graph,vertex_to_check,neighbor)
            F[neighbor] = (len(path) + F[vertex_to_check][0] , path)
    return F

print(find_longest_path(G,0,10))