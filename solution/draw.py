# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
from networkx import Graph
import matplotlib


def draw_graph_block(g: Graph, edges: list = None):
    matplotlib.use('MacOSX')

    if edges:
        for i, n in enumerate(edges):
            if i < len(edges) - 1:
                g.edges[edges[i], edges[i + 1]]['color'] = 'red'

    pos = nx.spring_layout(g, k=2)

    nx.draw_networkx_nodes(g, pos)
    nx.draw_networkx_labels(g, pos)
    nx.draw_networkx_edges(g, pos,
                           connectionstyle="arc3, rad=0.1",
                           edge_color=[d['color'] for x, y, d in g.edges(data=True)],
                           arrows=True)

    plt.show(block=True)


def draw_graph_to_file(g: Graph, edges: list = None, file_name='graph.png'):
    matplotlib.use('Agg')

    if edges:
        for i, n in enumerate(edges):
            if i < len(edges) - 1:
                g.edges[edges[i], edges[i + 1]]['color'] = 'red'

    pos = nx.spring_layout(g, k=2)

    nx.draw_networkx_nodes(g, pos)
    nx.draw_networkx_labels(g, pos)
    nx.draw_networkx_edges(g, pos,
                           connectionstyle="arc3, rad=0.1",
                           edge_color=[d['color'] for x, y, d in g.edges(data=True)],
                           arrows=True)

    plt.savefig(file_name, format="PNG", dpi=40)
    plt.clf()
