import networkx as nx

import link_analysis.api_module
import link_analysis.converters
import link_analysis.visualizer


setup_code = """\
import api_module
"""


def fit_graph(graph_json, node_size=2000):
    nodes = graph_json[0]
    edges = graph_json[1]

    # Filling the graph.
    nx_graph = nx.DiGraph()
    for node in nodes:
        nx_graph.add_node(node, node_size=node_size)

    nx_graph.add_weighted_edges_from(edges)
    return nx_graph


def get_graph(graph_name):
    graph_json = converters.load_json(graph_name)
    graph = fit_graph(graph_json)
    return graph


def save_and_check(graph, graph_name):
    check = converters.save_json(graph, graph_name)
    print(check)


def calc_betweenness_centrality():
    graph = get_graph("graph.json")
    result = nx.betweenness_centrality(graph)
    save_and_check(result, "betweenness_centrality.json")


def calc_pagerank():
    graph = get_graph("graph.json")
    result = nx.pagerank(graph)
    save_and_check(result, "pagerank.json")


def calc_closeness_centrality():
    graph = get_graph("graph.json")
    result = nx.closeness_centrality(graph)
    save_and_check(result, "closeness_centrality.json")


def calc_degree_centrality():
    graph = get_graph("graph.json")
    result = nx.degree_centrality(graph)
    save_and_check(result, "degree_centrality.json")


def calc_katz_centrality():
    graph = get_graph("graph.json")
    result = nx.katz_centrality(graph)
    save_and_check(result, "katz_centrality.json")


def load_and_sort(reverse=False):
    # Loads all calculated graph metrics.
    btwns_centrality = converters.load_json("betweenness_centrality.json")
    pagerank = converters.load_json("pagerank.json")
    cls_centrality = converters.load_json("closeness_centrality.json")
    degree_centrality = converters.load_json("degree_centrality.json")
    katz_centrality = converters.load_json("katz_centrality.json")

    # Sort them in specified order.
    btwns_centrality = sorted(btwns_centrality.items(), key=lambda x: x[1],
                              reverse=reverse)
    pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=reverse)
    cls_centrality = sorted(cls_centrality.items(), key=lambda x: x[1],
                            reverse=reverse)
    degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1],
                               reverse=reverse)
    katz_centrality = sorted(katz_centrality.items(), key=lambda x: x[1],
                             reverse=reverse)

    # Print Top-10.
    print(btwns_centrality[:10])
    print(pagerank[:10])
    print(cls_centrality[:10])
    print(degree_centrality[:10])
    print(katz_centrality[:10])

    # And save.
    save_and_check(btwns_centrality, "betweenness_centrality_sorted.json")
    save_and_check(pagerank, "pagerank_sorted.json")
    save_and_check(cls_centrality, "closeness_centrality_sorted.json")
    save_and_check(degree_centrality, "degree_centrality_sorted.json")
    save_and_check(katz_centrality, "katz_centrality_sorted.json")


def visualize(graph_name, n_nodes, n_edges):
    graph_json = converters.load_json(graph_name)
    visualizer.visualize_link_graph([graph_json[0][:n_nodes],
                                     graph_json[1][:n_edges]])


def smart_visualize(graph_name):
    sorted_result = converters.load_json(graph_name)
    print(sorted_result[0][0])
    api_module.start_process_with(sorted_result[0][0], 3,
                                  nodesIndegreeRange=(2, 1000),
                                  showPicture=True,
                                  visualizerParameters=(20, 8, (40, 40)))


def main():
    calc_betweenness_centrality()
    # calc_pagerank()
    # calc_closeness_centrality()
    # calc_degree_centrality()
    # calc_katz_centrality()
    # load_and_sort(True)
    # visualize("graph.json", 100, 100)
    # smart_visualize("betweenness_centrality_sorted.json")


if __name__ == "__main__":
    main()


# Get Top-5 from the head of the metric list and Top-5 from the tail of
# this one. We can skip some uninterested results in list.
BETWEENNESS_CENTRALITY_TOP = [
    "КСРФ_25-П_2012"      # 1
    "КСРФ_16-П_2013"      # 2
    "КСРФ_4-П_2010"       # 3
    "КСРФ_8-П_2013"       # 4
    "КСРФ_8-П_2014"       # 5
]
# ...
BETWEENNESS_CENTRALITY_BOTTOM = [
    "КСРФ_679-О_2017"     # n - 4
    "КСРФ_10-П_2003"      # n - 3
    "КСРФ_2927-О_2015"    # n - 2
    "КСРФ_1976-О_2015"    # n - 1
    "КСРФ_525-О_2005"     # n
]


PAGERANK_TOP = [
    "КСРФ_2-П_2007"       # 1
    "КСРФ_4-П_1996"       # 2
    "КСРФ_20-П_1998"      # 3
    "КСРФ_5-П_2005"       # 4
    "КСРФ_11-П_2002"      # 5
]
# ...
PAGERANK_BOTTOM = [
    "КСРФ_2015-О-Р_2016"  # n - 4
    "КСРФ_1908-О_2018"    # n - 3
    "КСРФ_970-О_2015"     # n - 2
    "КСРФ_10-П_2003"      # n - 1
    "КСРФ_2927-О_2015"    # n
]


CLOSENESS_CENTRALITY_TOP = [
    "КСРФ_4-П_1996"       # 1
    "КСРФ_5-П_2005"       # 2
    "КСРФ_2-П_2007"       # 3
    "КСРФ_20-П_1998"      # 4
    "КСРФ_5-П_1998"       # 5
]
# ...
CLOSENESS_CENTRALITY_BOTTOM = [
    "КСРФ_679-О_2017"     # n - 4
    "КСРФ_1799-О_2016"    # n - 3
    "КСРФ_970-О_2015"     # n - 2
    "КСРФ_10-П_2003"      # n - 1
    "КСРФ_2927-О_2015"    # n
]


DEGREE_CENTRALITY_TOP = [
    "КСРФ_2-П_2007"       # 1
    "КСРФ_11-П_2002"      # 2
    "КСРФ_4-П_2006"       # 3
    "КСРФ_4-П_1996"       # 4
    "КСРФ_3-П_2003"       # 5
]
# ...
DEGREE_CENTRALITY_BOTTOM = [
    "КСРФ_34-О_2005"      # n - 4
    "КСРФ_1799-О_2016"    # n - 3
    "КСРФ_970-О_2015"     # n - 2
    "КСРФ_10-П_2003"      # n - 1
    "КСРФ_2927-О_2015"    # n
]


KATZ_CENTRALITY_TOP = [
    "КСРФ_2-П_2007"       # 1
    "КСРФ_4-П_1996"       # 2
    "КСРФ_5-П_1998"       # 3
    "КСРФ_5-П_2005"       # 4
    "КСРФ_8-П_2014"       # 5
]
# ...
KATZ_CENTRALITY_BOTTOM = [
    "КСРФ_679-О_2017"     # n - 4
    "КСРФ_1799-О_2016"    # n - 3
    "КСРФ_970-О_2015"     # n - 2
    "КСРФ_10-П_2003"      # n - 1
    "КСРФ_2927-О_2015"    # n
]