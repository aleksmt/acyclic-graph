#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx

from solution.draw import draw_graph_to_file
from solution.graph import CycleFinder

if __name__ == '__main__':
    # Use with caution!

    for i in range(1, 100):
        vertices = i
        random_g = nx.fast_gnp_random_graph(vertices, 1.3 / vertices, directed=True)

        graph = CycleFinder(random_g)
        graph.has_cycle()

        draw_graph_to_file(random_g, graph.get_cycle(), file_name=f'graph_{i}.png')
