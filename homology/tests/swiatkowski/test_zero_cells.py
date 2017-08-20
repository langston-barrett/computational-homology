#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from homology.swiatkowski.zero_cells import *
from homology.tests.graph_hypothesis import random_graph
from hypothesis import strategies
from sage.graphs.graph import Graph
from math import factorial
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

@hypothesis.given(strategies.integers(min_value=0, max_value=6))
def test_zero_cells_star(n):
    """\
    There are P(n, n) = n! configurations of a n points on the interval.
    """
    assert sum(1 for _ in zero_cells(n, Graph([(0, 1)]))) == factorial(n)


@hypothesis.given(strategies.integers(min_value=0, max_value=2),
                  random_graph(max_vertices=5, max_edges=5))
@hypothesis.example(1, Graph([[0, 1]]))
@hypothesis.settings(max_examples=100)
def test_zero_cells(n, graph):
    """\
    In each configuration of n points on a random graph, all n points should be
    present on a vertex or an edge, and no point should be repeated. Further,
    configurations are just assignments of labels on G, they should be
    isomorphic to G.
    """
    for configuration in zero_cells(n, graph, logger=logger):

        # Gather a list of points on vertices
        on_vertices = []
        for vertex_label in configuration.vertices():
            try:
                on_vertices.append(vertex_label[1])
            except TypeError:
                pass

        points = list(itertools.chain(on_vertices, *configuration.edge_labels()))
        points_set = frozenset(points)

        assert configuration.is_isomorphic(graph)  # configurations are isomorphic
        assert points_set == frozenset(xrange(n))  # all points are present
        assert len(points) == len(points_set)  # no points are repeated
