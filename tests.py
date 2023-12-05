#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from typing import Union

import networkx as nx
from networkx import DiGraph

from solution import draw
from solution.graph import CycleFinder, GraphException


class TestGraphs(unittest.TestCase):

    show_graph_after_test = False
    di_g: Union[DiGraph, None] = None
    cf: Union[CycleFinder, None] = None

    def setUp(self) -> None:
        self.di_g = nx.DiGraph()
        self.cf = CycleFinder(self.di_g)

    def tearDown(self) -> None:
        self.di_g = None
        self.cf = None
        try:
            draw.draw_graph_block(self.di_g, self.cf.get_cycle())
        except GraphException:
            if self.show_graph_after_test and self.cf.has_cycle():
                draw.draw_graph_block(self.di_g, self.cf.get_cycle())

    def test_no_cycle_graph(self):
        self.di_g.add_edge(0, 1)
        self.di_g.add_edge(1, 2)

        self.assertFalse(self.cf.has_cycle())
        self.assertEqual(self.cf.get_cycle(), None)

    def test_simple_cycle_graph(self):
        self.di_g.add_edge(0, 1)
        self.di_g.add_edge(1, 2)
        self.di_g.add_edge(2, 0)

        self.assertTrue(self.cf.has_cycle())
        self.assertListEqual(self.cf.get_cycle(), [0, 1, 2, 0])

    def test_simple_loop_graph(self):
        self.di_g.add_edge(0, 0)

        self.assertTrue(self.cf.has_cycle())
        self.assertListEqual(self.cf.get_cycle(), [0, 0])

    def test_loop_near_dangling_random_graph(self):
        self.di_g = nx.fast_gnp_random_graph(9, 0, directed=True)
        self.di_g.add_edge(20, 20)

        self.assertTrue(self.cf.has_cycle())
        self.assertListEqual(self.cf.get_cycle(), [20, 20])

    def test_big_graph(self):
        self.di_g.add_edge(0, 1)
        self.di_g.add_edge(1, 7)
        self.di_g.add_edge(7, 2)
        self.di_g.add_edge(7, 5)
        self.di_g.add_edge(2, 5)
        self.di_g.add_edge(2, 4)
        self.di_g.add_edge(3, 4)
        self.di_g.add_edge(5, 6)
        self.di_g.add_edge(2, 0)

        self.assertTrue(self.cf.has_cycle())
        self.assertListEqual(self.cf.get_cycle(), [0, 1, 7, 2, 0])

    def test_cycle_in_dangling_graph(self):
        # graph 1 (no cycle)
        self.di_g.add_edge(0, 1)
        self.di_g.add_edge(1, 7)
        self.di_g.add_edge(7, 2)
        self.di_g.add_edge(7, 5)
        self.di_g.add_edge(2, 5)
        self.di_g.add_edge(2, 4)
        self.di_g.add_edge(3, 4)
        self.di_g.add_edge(5, 6)
        self.di_g.add_edge(2, 3)

        # graph 2 (dangling with cycle)
        self.di_g.add_edge(8, 9)
        self.di_g.add_edge(9, 10)
        self.di_g.add_edge(10, 8)

        self.assertTrue(self.cf.has_cycle())
        self.assertListEqual(self.cf.get_cycle(), [8, 9, 10, 8])

    def test_cycle_in_letters_graph(self):
        # graph 3 (letters)
        self.di_g.add_edge('A', 'B')
        self.di_g.add_edge('B', 'C')
        self.di_g.add_edge('C', 'A')

        self.assertTrue(self.cf.has_cycle())
        self.assertListEqual(self.cf.get_cycle(), ['A', 'B', 'C', 'A'])

    def test_cycle_in_mixed_vertex_type_groups_graph(self):
        # graph 1 (digits)
        self.di_g.add_edge(0, 1)
        self.di_g.add_edge(1, 7)
        self.di_g.add_edge(7, 2)
        self.di_g.add_edge(7, 5)
        self.di_g.add_edge(2, 5)
        self.di_g.add_edge(2, 4)
        self.di_g.add_edge(3, 4)
        self.di_g.add_edge(5, 6)
        self.di_g.add_edge(2, 3)

        # graph 2 (digits)
        self.di_g.add_edge(8, 9)
        self.di_g.add_edge(9, 10)
        self.di_g.add_edge(10, 8)

        # graph 3 (letters)
        self.di_g.add_edge('A', 'B')
        self.di_g.add_edge('B', 'C')
        self.di_g.add_edge('C', 'A')

        self.assertTrue(self.cf.has_cycle())
        self.assertListEqual(self.cf.get_cycle(), [8, 9, 10, 8])

    def test_cycle_in_mixed_vertex_graph(self):
        self.di_g.add_edge(0, 1)
        self.di_g.add_edge(1, 'A')
        self.di_g.add_edge('A', 'B')
        self.di_g.add_edge('B', 0)

        self.assertTrue(self.cf.has_cycle())
        self.assertListEqual(self.cf.get_cycle(), [0, 1, 'A', 'B', 0])

    def test_cycle_with_bi_directed_edges_graph(self):
        self.di_g.add_edge(0, 1)
        self.di_g.add_edge(0, 4)
        self.di_g.add_edge(0, 2)
        self.di_g.add_edge(0, 3)
        self.di_g.add_edge(4, 1)
        self.di_g.add_edge(2, 4)
        self.di_g.add_edge(3, 0)

        self.assertTrue(self.cf.has_cycle())
        self.assertListEqual(self.cf.get_cycle(), [0, 3, 0])

    def test_no_cycle_tree_with_many_terminal_vertices_graph(self):
        self.di_g.add_edge(1, 2)
        self.di_g.add_edge(1, 3)
        self.di_g.add_edge(2, 5)
        self.di_g.add_edge(2, 6)
        self.di_g.add_edge(3, 4)  # terminal
        self.di_g.add_edge(3, 7)
        self.di_g.add_edge(3, 8)
        self.di_g.add_edge(5, 9)
        self.di_g.add_edge(6, 10)
        self.di_g.add_edge(7, 11)
        self.di_g.add_edge(8, 12)
        self.di_g.add_edge(9, 14)
        self.di_g.add_edge(10, 15)
        self.di_g.add_edge(11, 15)
        self.di_g.add_edge(12, 13)  # terminal
        self.di_g.add_edge(12, 16)
        self.di_g.add_edge(14, 17)  # terminal
        self.di_g.add_edge(14, 18)  # terminal
        self.di_g.add_edge(14, 19)
        self.di_g.add_edge(15, 20)  # terminal
        self.di_g.add_edge(15, 21)
        self.di_g.add_edge(16, 22)  # terminal
        self.di_g.add_edge(16, 23)  # terminal
        self.di_g.add_edge(16, 26)
        self.di_g.add_edge(19, 24)
        self.di_g.add_edge(19, 24)
        self.di_g.add_edge(21, 25)
        self.di_g.add_edge(24, 29)
        self.di_g.add_edge(24, 28)  # terminal
        self.di_g.add_edge(25, 29)
        self.di_g.add_edge(26, 27)  # terminal
        self.di_g.add_edge(29, 30)  # terminal

        self.assertFalse(self.cf.has_cycle())
        self.assertEqual(self.cf.get_cycle(), None)

    def test_read_no_cycle_graph_from_file(self):
        self.di_g = nx.read_graphml('graphs/directed-nocycle.xml')

        self.assertFalse(self.cf.has_cycle())
        self.assertEqual(self.cf.get_cycle(), None)

    def test_read_cycle_graph_from_file(self):
        self.di_g = nx.read_graphml('graphs/directed-cycle.xml')

        self.assertTrue(self.cf.has_cycle())
        self.assertListEqual(self.cf.get_cycle(), ['B', 'C', 'F', 'G', 'B'])

    def test_check_exception_before_reading_graph(self):
        di_g = nx.DiGraph()
        cf = CycleFinder(di_g)

        with self.assertRaises(GraphException):
            cf.get_cycle()


if __name__ == '__main__':
    unittest.main()
