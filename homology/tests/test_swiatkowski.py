#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from functools import partial
from homology.swiatkowski import subdivide, zero_cells, _zero_cells_with_duplicates
from homology.tests.graph_hypothesis import random_graph
from hypothesis import strategies
from sage.graphs.graph import Graph
import hypothesis
import pytest

# For debugging functions that aren't working
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler(filename="debug.log", mode="w"))


@hypothesis.given(random_graph(max_vertices=10, max_edges=20),
                  strategies.integers(min_value=0, max_value=10))
def test_subdivide(graph, n):
    """ Labeling the edges doesn't change how many there are """
    assert len(subdivide(n, graph).edges()) == graph.size()

def test__zero_cells_with_duplicates():
    f = lambda gs: list(map(lambda x: x.edges(), gs))
    test = partial(_zero_cells_with_duplicates, logger=logger)
    assert f(test(2, Graph([(0, 1)]))) == [(0, 1, [0]), (0, 1, [0])]
