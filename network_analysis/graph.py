import link_analysis as l
import web_crawler
import networkx as nx
import matplotlib.pyplot as plt


path_to_graph = 'graph.json'
betwenes = ["КСРФ/25-П/2012", "КСРФ/16-П/2013", "КСРФ/4-П/2010", "КСРФ/8-П/2013", "КСРФ/8-П/2014"]
# betwenes = ["КСРФ/25-П/2012", "КСРФ/16-П/2013", "КСРФ/4-П/2010"]

allow_nodes = set(betwenes)

graph = l.converters.load_json(path_to_graph)
print('point0')
for i in range(1):
    print('point1 ' + str(i))
    for edge in graph[1]:
        if edge[0] in allow_nodes and\
                edge[1] in allow_nodes:
            continue

        if edge[0] in betwenes:
            allow_nodes.add(edge[1])
        if edge[1] in betwenes:
            allow_nodes.add(edge[0])

new_graph = [[], []]
print('point2')

for node in graph[0]:
    if node in allow_nodes and node not in betwenes:
        new_graph[0].append(node)
print('point3')
            
for edge in graph[1]:
    if edge[0] in allow_nodes and\
       edge[1] in allow_nodes:
        new_graph[1].append(edge)
print('point4')


nodes = new_graph[0]
edges = new_graph[1]


nodeSize=200
fontSize=3
pictureSize=(70, 70)

# filling the graph
nxGraph = nx.DiGraph()
nxGraph.add_weighted_edges_from(edges)

# drawing the graph
plt.figure(figsize=pictureSize)
pos = nx.fruchterman_reingold_layout(nxGraph)
nx.draw_networkx_nodes(nxGraph, pos,  node_size=nodeSize, nodelist=nodes, node_color='r')
nx.draw_networkx_nodes(nxGraph, pos,  node_size=5*nodeSize, nodelist=betwenes, node_color='b')

labels = {node: node for node in betwenes}
nx.draw_networkx_labels(nxGraph, pos, labels,
                        font_size=fontSize, font_color='r')

nx.draw_networkx_edges(nxGraph, pos)
plt.savefig('fig.eps', format='eps', dpi=1000)
# plt.show()

print('point5')

