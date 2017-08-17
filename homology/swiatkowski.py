# -*- coding: utf-8 -*-
"""\
Swiatkowski describes a deformation retraction of UConf_n(Γ) which has
dimension min(b(Γ), n) (where b(Γ) is the number of branched vertices of Γ,
i.e. those of valence three or greater). Daniel Lütgehetmann extends this to a
deformation retraction of Conf_n(Γ) in their master's thesis.
"""

import sage.all
import logging
import itertools
import functools

# Ensure we've got chomp
from sage.interfaces.chomp import have_chomp
assert have_chomp() is True

# Logging configuration: by default, produce no output
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def unique_everseen(iterable, key=None):
    """ List unique elements, preserving order. Remember all elements ever seen.

    Code from the "Itertools Recipes" section of the Python documentation.

    Examples:
        >>> list(unique_everseen('AAAABBBCCDAABBB'))
        ['A', 'B', 'C', 'D']
        >>> list(unique_everseen('ABBCcAD', str.lower))
        ['A', 'B', 'C', 'D']

    """
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def update(d, other):
    d.update(other)
    return d

chain_dicts = lambda lst: functools.reduce(update, lst, {})


def _label_lookup_table(G):
    """ A dictionary with labels as keys and the edges they occupy as values

    Examples:

        >>> from sage.graphs.graph import Graph
        >>> _label_lookup_table(Graph([]))
        {}

    TODO: comprehension?
    """
    dic = dict()
    for u, v, labels in G.edges(labels=True):
        for label in labels:
            dic[label] = (u, v)
    return dic


def _zero_cells_with_duplicates(n, G, logger=logger):
    """ A generator of configurations of n points on G

    The implementation causes duplicates, see ``zero_cells`` for a version
    without duplicates, and for more documentation.

    Examples:

        >>> from sage.graphs.graph import Graph
        >>> edges_list = lambda gs: list(map(lambda x: x.edges(), gs))
        >>> edges_list(_zero_cells_with_duplicates(1, Graph([(0, 1)])))
        [[(0, 1, [0])], [(0, 1, [0])]]

        >>> edges_list(_zero_cells_with_duplicates(2, Graph([(0, 1)])))
        [(0, 1, [0]), (0, 1, [0])]

    """

    G = subdivide(n, G)
    logger.debug("Graph: {}".format(G))

    # Look up which edge a label lies on. Construction is O(n*E).
    lookup = _label_lookup_table(G)
    logger.debug("Lookup: {}".format(lookup))

    # A list of every available label on this graph. Construction is O(n*E).
    labels = itertools.chain((n for n in xrange(G.order())), *G.edge_labels())
    logger.debug("Labels: {}".format(list(labels)))


    # We'll yield a copy of G with the appropriate labels
    H = sage.all.copy(G)

    logger.debug("Labels: {}".format(list(labels)))
    perms = itertools.permutations(labels, n)
    logger.debug("Permutations: {}".format(list(perms)))
    # Loop through all n-tuples of point positions
    for perm in perms:

        # Zero out labels
        for u, v in H.edges(labels=False):
            H.set_edge_label(u, v, [])

        # For each point, record its location on the graph
        relabeling = {n: (n, None) for n in range(H.order())}
        for point, location in enumerate(perm):
            # If it's on a vertex, relabel the vertex
            if location < H.order():
                relabeling[location] = (location, point)
            # Otherwise, look up the appropriate edge and append it
            else:
                u, v = lookup[location]
                current_label = H.edge_label(u, v)
                H.set_edge_label(u, v, current_label + [point])

        yield H.copy(immutable=True)


def zero_cells(n, G):
    """ Get configurations of n points on G

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

        >>> list(zero_cells(1, Graph([(0, 1)])))
    """
    return unique_everseen(_zero_cells_with_duplicates(n, G))


def subdivide(n, G):
    """ Give labels to the branched vertices and edges of G.

    Each edge is given a label that is a ``frozenset`` of length n, ordered by the
    usual ``<``. Vertices are already labeled in G. This is kind of a
    bastardized Abrams-style model.

        >>> from sage.graphs.graph import Graph
        >>> subdivide(1, Graph({})).edges(labels=True)
        []

        >>> subdivide(1, Graph([(0, 1)])).edges(labels=True)  # G := 0--1
        [(0, 1, frozenset([2, 3]))]

        >>> subdivide(2, Graph([(0, 1), (1, 2), (2, 0)])).edges(labels=True)
        [(0, 1, frozenset([3, 4, 5])), ..., (1, 2, frozenset([9, 10, 11]))]
    """

    ORDER = G.order()  # each edge has as many labels as there are vertices
    current = G.order()
    for u, v in G.edges(labels=False):
        G.set_edge_label(u, v, frozenset((n for n in xrange(current, current+ORDER))))
        current += ORDER

    return G



def swiatkowski_model(n, G):
    """ Returns the Swiatkowski model of the Conf_n(G) """
    assert G.is_undirected()
    assert all(map(lambda d: d != 2, G.degree()))  # no inessential vertices
