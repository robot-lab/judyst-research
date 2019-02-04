import json
import link_analysis as l
import web_crawler
import networkx as nx
import matplotlib.pyplot as plt


def save_csv_betwenese_part():
   
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
    f = open('graph_nodes.csv', 'wt', encoding='utf-8')
    f.write('Id; Label\n')
    for node in nodes:
        f.write(node + ';' + "\"" + node + "\"\n")
    for node in betwenes[0]:
        f.write(node + ';' + "\"" + node + "\"\n")
    f.close()
    f = open('graph_edges.csv', 'wt', encoding='utf-8')
    f.write('Source; Target\n')
    for edge in edges:
        f.write(edge[0] + ';' + edge[1] + '\n')
    f.close()


def save_csv_all_graph():
    f = open('graph.json', 'rt', encoding='utf-8')
    s = f.read()
    graph = json.loads(s)
    f.close()
    f = open('graph_nodes.csv', 'wt', encoding='utf-8')
    f.write('Id; Label\n')
    for node in graph[0]:
        f.write(node + ';' + "\"" + node + "\"\n")
    f.close()
    f = open('graph_edges.csv', 'wt', encoding='utf-8')
    f.write('Source; Target\n')
    for edge in graph[1]:
        f.write(edge[0] + ';' + edge[1] +'\n')
    f.close()
    

if __name__ == '__main__':
#    save_csv_betwenese_part()
    save_csv_all_graph()