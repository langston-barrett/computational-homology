# -*- coding: utf-8 -*-
"""\
Generate the 0-cells, or configurations, of n points on a graph in the
Swiatkowski model.
"""
import sage.all
import logging
import itertools
from homology.swiatkowski.graph_util import edge_label_fold

# Logging configuration: by default, produce no output
default_logger = logging.getLogger(__name__)
default_logger.addHandler(logging.NullHandler())


def subdivide(n, G):
    """ Give labels to the branched vertices and edges of G.

    Each edge is given a label that is a ``frozenset`` of length n, ordered by the
    usual ``<``. Vertices are already labeled in G. This subdivision mirrors
    what happens in the Abrams model.

        >>> from sage.graphs.graph import Graph
        >>> subdivide(1, Graph({})).edges(labels=True)
        []

        >>> subdivide(1, Graph([(0, 1)])).edges(labels=True)  # G := 0--1
        [(0, 1, frozenset([2]))]

        >>> subdivide(2, Graph([(0, 1)])).edges(labels=True)  # G := 0--1
        [(0, 1, frozenset([2, 3]))]

        >>> subdivide(2, Graph([(0, 1), (1, 2), (2, 0)])).edges(labels=True)
        [(0, 1, frozenset([3, 4])), ..., (1, 2, frozenset([8, 7]))]
    """
    return edge_label_fold(
        lambda label, acc: (frozenset(xrange(acc, acc + n)), acc + n),
        G.order(), G)[0]


def invert_permutation(tup):
    """\
    Given an n-tuple, make a dict with elements for keys and indices for values
    """
    return {value: index for index, value in enumerate(tup)}


def _permutation_to_vertex_relabel(permutation, G):
    """\
    Get a dictionary of new labels for vertices based on a permutation of the
    points on an Abrams-subdivision of G.

    Runtime: O(V+n)
    """
    relabeling = dict()
    for point, position in enumerate(permutation):
        # If the point is on a vertex, then the key will exist
        try:
            relabeling[position] = (position, point)
        except KeyError:
            pass

    return frozenset(relabeling.items())


def _permutation_to_edge_relabel(permutation, G):
    """\
    Get new labels for each edge based on a permutation of the points on an
    Abrams-subdivision of G.

    Runtime: O(En)
    """
    inverted = invert_permutation(permutation)
    for u, v, labels in G.edges(labels=True):
        new_label = []
        for label in labels:
            # If a label is a key in the inverted permutation, there is a
            # point on it. Thus, we should append that point to the label.
            try:
                new_label.append(inverted[label])
            except KeyError:
                pass
        yield (u, v, tuple(new_label))


def zero_cells(n, G, logger=default_logger):
    """ A generator of configurations of n points on G

    They are encoded as copies of G with vertices and edges labeled by which
    points are on them. The (branched) vertices can only have one point
    occupying them, so they are either labeled as:

     * ``(n, None)``: No point is on vertex n
     * ``(n, m)``: The point with label m is on vertex n

    The edges can have n points on them. The edge labels are (ordered) lists of
    combined length <= n.

    Examples:

     * There are no configurations on an empty graph:

        >>> from sage.graphs.graph import Graph
        >>> list(zero_cells(1, Graph({})))
        []

     * Up to homotopy, there is one configuration of a point on the interval:

        >>> get_edges = lambda cnfgs: map(lambda G: G.edges(), cnfgs)
        >>> I = Graph([(0, 1)])
        >>> list(get_edges(zero_cells(1, I)))
        [[(0, 1, (0,))]]

     * There are two configurations of two points on the interval:

        >>> sorted(list(get_edges(zero_cells(2, I))))
        [[(0, 1, (0, 1))], [(0, 1, (1, 0))]]

     * One point on the Y can be on any leg or on the central vertex:

        >>> from sage.all import *
        >>> sum(1 for _ in zero_cells(1, graphs.StarGraph(3)))
        4

    Implementation: the graph is subdivided Abrams-style, so that each edge has
    n additional labels on it. We loop through the permutations of n points on
    these n+(n*E) labels.

     * If the label represents a vertex, that vertex is renamed as a tuple
       (original_label, point_on_this_vertex).
     * If the label represents a vertex, we append that point to the list of
       points on that edge. This is done with order kept in mind, see
       _permutation_to_edge_relabel.

    """
    logger.debug("n: {}".format(n))

    G = subdivide(n, G)
    logger.debug("Graph: {}".format(G))

    # A list of every available label on this graph. Construction is O(n*E).
    branched_vertices = (n for n, deg in enumerate(G.degree()) if deg >= 3)
    labels = itertools.chain(branched_vertices, *G.edge_labels())
    labels = list(labels)
    logger.debug("Labels: {}".format(labels))

    # We'll yield a copy of G with the appropriate labels
    H_ = sage.all.copy(G)

    perms = itertools.permutations(labels, n)
    perms = list(perms)
    logger.debug("Permutations: {}".format(list(perms)))

    # Loop through all n-tuples of point positions
    # Gather necessary relabelings of H
    relabeling_set = set()
    for perm in perms:
        vertex_relabel = _permutation_to_vertex_relabel(perm, G)
        edge_relabel = _permutation_to_edge_relabel(perm, G)
        relabeling_set.add((vertex_relabel, edge_relabel))

    # Only unique relabelings will be yielded
    for (vertex_relabel, edge_relabel) in relabeling_set:
        H = sage.all.copy(H_)

        for (u, v, new_label) in edge_relabel:
            H.set_edge_label(u, v, new_label)

        H.relabel(dict(vertex_relabel))
        yield H.copy(immutable=True)
