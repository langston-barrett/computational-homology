# -*- coding: utf-8 -*-
"""\
Generate the 0-cells, or configurations, of n particles on a graph in the
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

    Each edge is given a label that is a pair (start, end). This represents the
    interval [start, end] in the integers. Vertices are already labeled in G.
    This subdivision mirrors what happens in the Abrams model.

        >>> from sage.graphs.graph import Graph
        >>> subdivide(1, Graph({})).edges(labels=True)
        []

        >>> subdivide(1, Graph([(0, 1)])).edges(labels=True)  # G := 0--1
        [(0, 1, (2, 2))]

        >>> subdivide(2, Graph([(0, 1)])).edges(labels=True)  # G := 0--1
        [(0, 1, (2, 3))]

        >>> subdivide(3, Graph([(0, 1), (1, 2), (2, 0)])).edges(labels=True)
        [(0, 1, (3, 5)), ..., (1, 2, (9, 11))]
    """
    return edge_label_fold(
        lambda label, acc: ((acc, acc + n - 1), acc + n),
        G.order(), G)[0]


def invert_permutation(tup):
    """\
    Given an n-tuple, make a dict with elements for keys and indices for values
    """
    return {value: index for index, value in enumerate(tup)}


def _permutation_to_vertex_relabel(permutation, G):
    """\
    Get a dictionary of new labels for vertices based on a permutation of the
    particles on an Abrams-subdivision of G.

    Runtime: O(V+n)
    """
    relabeling = dict()
    for particle, position in enumerate(permutation):
        # If the particle is on a vertex, then the key will exist
        try:
            relabeling[position] = (position, particle)
        except KeyError:
            pass

    return frozenset(relabeling.items())


def _permutation_to_edge_relabel(permutation, G):
    """\
    Get new labels for each edge based on a permutation of the particles on an
    Abrams-subdivision of G.

    Runtime: O(En)
    """
    inverted = invert_permutation(permutation)
    for u, v, endpoints in G.edges(labels=True):
        new_label = []
        # The interval on the edge is inclusive, so we have to add 1 to the end
        for label in xrange(endpoints[0], endpoints[1] + 1):
            # If a label is a key in the inverted permutation, there is a
            # particle on it. Thus, we should append that particle to the label.
            try:
                # TODO: replace edge labels with their endpoints in subdivision
                new_label.append(inverted[label])
            except KeyError:
                pass
        yield (u, v, tuple(new_label))


def zero_cells(n, G, logger=default_logger):
    """ A generator of configurations of n particles on G

    They are encoded as copies of G with vertices and edges labeled by which
    particles are on them. The (branched) vertices can only have one particle
    occupying them, so they are either labeled as:

     * ``(n, None)``: No particle is on vertex n
     * ``(n, m)``: The particle with label m is on vertex n

    The edges can have n particles on them. The edge labels are (ordered) lists of
    combined length <= n.

    Examples:

     * There are no configurations on an empty graph:

        >>> from sage.graphs.graph import Graph
        >>> list(zero_cells(1, Graph({})))
        []

     * Up to homotopy, there is one configuration of a particle on the interval:

        >>> get_edges = lambda cnfgs: map(lambda G: G.edges(), cnfgs)
        >>> I = Graph([(0, 1)])
        >>> list(get_edges(zero_cells(1, I)))
        [[(0, 1, (0,))]]

     * There are two configurations of two particles on the interval:

        >>> sorted(list(get_edges(zero_cells(2, I))))
        [[(0, 1, (0, 1))], [(0, 1, (1, 0))]]

     * One particle on the Y can be on any leg or on the central vertex:

        >>> from sage.all import *
        >>> sum(1 for _ in zero_cells(1, graphs.StarGraph(3)))
        4

    Implementation: the graph is subdivided Abrams-style, so that each edge has
    n additional labels on it. We loop through the permutations of n particles on
    these n+(n*E) labels.

     * If the label represents a vertex, that vertex is renamed as a tuple
       (original_label, particle_on_this_vertex).
     * If the label represents a vertex, we append that particle to the list of
       particles on that edge. This is done with order kept in mind, see
       _permutation_to_edge_relabel.

    """
    assert not G.is_directed()

    logger.debug("n: {}".format(n))
    G = subdivide(n, G)
    logger.debug("Graph: {}".format(G))

    # A list of every available label on this graph. Construction is O(n*E).
    branched = (v for v, deg in zip(G.vertices(), G.degree()) if deg >= 3)
    labels = itertools.chain(branched, *G.edge_labels())
    labels = list(labels)
    logger.debug("Labels: {}".format(labels))

    # Loop through all n-tuples of particle positions
    # Gather necessary relabelings of H
    relabeling_set = set()
    for perm in itertools.permutations(labels, n):
        vertex_relabel = _permutation_to_vertex_relabel(perm, G)
        # We need to make a set out of the edge relabel because it is a
        # generator object, whose hash doesn't reflect its content.
        edge_relabel = frozenset(_permutation_to_edge_relabel(perm, G))
        relabeling_set.add((vertex_relabel, edge_relabel))

    logger.debug("Relabeling set: {}".format(relabeling_set))

    # Only unique relabelings will be yielded
    for (vertex_relabel, edge_relabel) in relabeling_set:
        H = sage.all.copy(G)

        for (u, v, new_label) in edge_relabel:
            H.set_edge_label(u, v, new_label)

        H.relabel(dict(vertex_relabel))
        yield H.copy(immutable=True)
