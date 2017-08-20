"""\
Utilities for working with graphs in Sage, particularly ones with labeled edges.
"""
from __future__ import print_function
import sage.all
from sage.graphs.graph import Graph

class HashableGraph(Graph):
    """ A subclass of Sage's Graph which includes labels in its hash

     * Sage default behavior:

        >>> IGraph = lambda *args: Graph(*args, immutable=True)
        >>> hash(IGraph([(0, 1)])) == hash(IGraph([(0, 1)]))
        True
        >>> hash(IGraph([(0, 1, "x")])) == hash(IGraph([(0, 1, "y")]))
        True

     * HashableGraph:

        >>> hash(HashableGraph([(0, 1)])) == hash(HashableGraph([(0, 1)]))
        True
        >>> hash(HashableGraph([(0, 1, "x")])) == hash(HashableGraph([(0, 1, "y")]))
        False
    """

    def __hash__(self):
        try:
            return hash(frozenset(self.vertices() + self.edges(labels=True)))

        # If the labels were unhashable (probably lists), make them frozensets
        except TypeError as e:
            edges = map(lambda t: (t[0], t[1], frozenset(t[2])),
                        self.edges(labels=True))
            return hash(frozenset(self.vertices() + edges))


def edge_label_fold(f, accumulator, G):
    """ Fold over the edges labels of G using f.

    Inputs:
     * f: A function of two inputs, the first of which is the type of the edge
       labels of G, and the second of which is the type of the accumulator.
       Should output a new accumulator, or optionally a tuple of (new_label,
       new_accumulator).
     * accumulator: anything
     * G: A graph with labels

    Returns: A copy of the graph with new labels and the final accumulator.

    Examples:

        >>> from sage.graphs.graph import Graph
        >>> f = lambda label, acc: (None, acc + label)
        >>> edge_label_fold(f, "", Graph([(0, 1, "a"), (1, 2, "b")]))[1]
        'ab'
    """
    H = sage.all.copy(G)
    for (u, v, label) in H.edges(labels=True):
        accumulator = f(label, accumulator)
        try:
            new_label, accumulator = accumulator  # try to unpack a tuple
            H.set_edge_label(u, v, new_label)
        except TypeError:  # f didn't output a new label, but that's ok
            pass

    return H, accumulator


def edge_label_map(f, G):
    """ Apply a function to each of the labels in G, updating them

    Examples:

        >>> from sage.graphs.graph import Graph
        >>> I = Graph([(0, 1, "label")])
        >>> edge_label_map(lambda str: str + " woot", I).edges(labels=True)
        [(0, 1, 'label woot')]
    """
    return edge_label_fold(lambda label, acc: (f(label), None), None, G)[0]
