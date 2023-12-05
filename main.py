#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

import networkx as nx
from solution.draw import draw_graph_block
from solution.graph import CycleFinder

if __name__ == '__main__':
    # Example of running graph solver solution without tests
    # shows output to the stdout and opens pop-up using matplotlib

    parser = argparse.ArgumentParser(description='Cycle detection using DFS')
    parser.add_argument('v', type=int, nargs='?', default=10)
    args = parser.parse_args()

    vertices = args.v
    random_g = nx.fast_gnp_random_graph(vertices, 1.3 / vertices, directed=True)

    graph = CycleFinder(random_g)

    if graph.has_cycle():
        print(f'Graph has a cycle: {"->".join(map(str, graph.get_cycle()))}')
    else:
        print('Graph has no cycle')

    print(f'Total number of nodes = {len(random_g.nodes)}, edges = {len(random_g.edges)}')

    draw_graph_block(random_g, graph.get_cycle())
