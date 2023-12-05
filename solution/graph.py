# -*- coding: utf-8 -*-

from collections import deque
from typing import Union

from networkx import Graph


class CycleFinder:

    def __init__(self, g: Graph):
        self.g: Graph = g
        self.backtrack_sequence = deque()
        self.cycle_sequence: Union[None, list] = None
        self.tracking_final: Union[None, int] = None
        self.tracking_flag = True

    def has_cycle(self) -> bool:
        """ Returns true if graph is cyclic, else false """
        # Adding required attributes to a nodes
        for n in self.g.nodes().values():
            n['visited'] = False
        for n in self.g.edges().values():
            n['color'] = 'black'
        self.cycle_sequence = []

        # Recur and iterate over each node
        for node, attr in self.g.nodes(data=True):
            if not attr['visited']:
                if self._neighbour_lookup(node):
                    self.cycle_sequence.reverse()
                    self.cycle_sequence.append(self.cycle_sequence[0])
                    return True
        return False

    def get_cycle(self) -> Union[list, None]:
        """ Returns steps sequence "as is", e.g. [a, b, c, a] """
        if self.cycle_sequence is None:
            raise GraphException('First, you need to run has_cycle() method in order to get a result')
        return self.cycle_sequence if self.cycle_sequence else None

    def _neighbour_lookup(self, node) -> bool:
        """ Main recur cycle, implements DFS (Deep First Search) """
        # Mark current node as visited and adds to recursion stack
        self.g.nodes[node]['visited'] = True
        self.backtrack_sequence.append(node)

        # Recur for all neighbours and if any neighbour
        # is visited and in sequence, then graph is cyclic
        # also setting track data to record the path
        for neighbour in self.g.neighbors(node):
            if not self.g.nodes[neighbour]['visited']:
                if self._neighbour_lookup(neighbour):
                    if self.tracking_flag:
                        self.tracking_flag = False if node == self.tracking_final else True
                        self.cycle_sequence += [node]
                    return True
            elif neighbour in self.backtrack_sequence:
                self.tracking_final = neighbour
                self.cycle_sequence = [node]
                return True

        # Cleaning up the sequence of neighbours before starting the next loop
        self.backtrack_sequence.pop()
        return False


class GraphException(Exception):
    pass
