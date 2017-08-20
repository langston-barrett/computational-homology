#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from homology.swiatkowski.zero_cells import *
from homology.tests.graph_hypothesis import random_graph
from hypothesis import strategies
from sage.graphs.graph import Graph
import sage.all
import hypothesis
import itertools

# For debugging functions that aren't working
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler(filename="debug.log", mode="w"))


@hypothesis.given(strategies.integers(min_value=0, max_value=10),
                  random_graph(max_vertices=10, max_edges=20))
@hypothesis.example(0, Graph([[0, 1]]))
def test_subdivide(n, graph):
    subdivided = subdivide(n, graph)
    assert subdivided.is_isomorphic(graph)
    for (u, v, label) in subdivided.edges(labels=True):
        assert len(label) == n


@hypothesis.given(strategies.integers(min_value=3, max_value=25))
def test_zero_cells_star(n):
    """\
    There are n + 1 configurations of a single point on the nth star graph, one
    for each leg plus one for the central vertex.
    """
    assert sum(1 for _ in zero_cells(1, sage.all.graphs.StarGraph(n))) == n + 1


# TODO: uncomment me
# @hypothesis.given(strategies.integers(min_value=0, max_value=2),
#                   random_graph(max_vertices=5, max_edges=5))
# @hypothesis.example(1, Graph([[0, 1]]))
# @hypothesis.settings(max_examples=100)
# def test__zero_cells_with_duplicates(n, graph):
#     for configuration in _zero_cells_with_duplicates(n, graph, logger=logger):
#         # Configurations are just labelings, they should be isomorphic
#         assert configuration.is_isomorphic(graph)

#         # There should be a combined total of n points on edges and vertices
#         on_vs = filter(lambda t: t[1] is not None, configuration.vertices())
#         on_es = list(itertools.chain(*configuration.edge_labels()))
#         assert len(on_vs) + len(on_es) == n
