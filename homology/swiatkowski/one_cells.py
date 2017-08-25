# -*- coding: utf-8 -*-
"""\
Generate the 1-cells, or movements of a single particle, in the Swiatkowski
model.

The 1-cells are represented as...wait for it...a graph! The 0-cells are
the vertices and the one-cells are the edges between them. The graph is
naturally undirected: if you can move a particle, you can undo that movement
(move it back).
"""
import logging
import itertools

# Logging configuration: by default, produce no output
default_logger = logging.getLogger(__name__)
default_logger.addHandler(logging.NullHandler())


def get_moves_of_particle(zero_cell, particle, position):
    """ Get a list of moves that this particle can make

    Inputs:
     * zero_cell: A configuration of n particles on the graph
     * particle: The particle's label
     * position: Either a 2-tuple representing a branched vertex, or a 3-tuple
       representing an edge.

    Outputs: ???
    """


def get_moves_from(zero_cell):
    """ Get all possible moves (1-cells) emanating from this configuration """
    f = functools.partial(get_moves_of_vertex, zero_cell)

    # Get the moves of particles on branched vertices
    branched = (v for v, deg in zip(zero_cell.vertices(), zero_cell.degree())
                if deg >= 3)
    for vertex in branched:
        try:  # get the moves for the particle on this vertex
            particle = vertex[1]
            yield get_moves_of_particle(zero_cell, particle, vertex)
        except TypeError:  # there is no particle on this vertex
            pass

    for u, v, label in zero_cell.edges(labels=True):
        # TODO
        pass


def one_cells(zero_cells, logger=default_logger):
    """ Given the 0-cells of a graph, what are the 1-cells? """
    assert all(map(lambda g: not g.is_directed(), zero_cells))

    for zero_cell in zero_cells:
        moves = get_moves_from(zero_cell)
