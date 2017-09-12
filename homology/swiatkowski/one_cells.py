# -*- coding: utf-8 -*-
"""\
Generate the 1-cells, or movements of a single particle, in the Świątkowski
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
    if len(position) == 2:  # we're on a branched vertex
        # TODO

    if len(position) == 3:  # we're on an edge
        label = position[2]

        move_to = None
        # If we're at the first position, we can move to the initial vertex
        if label[0] == particle:
            move_to = position[0]

        # If we're at the last postition, we can move to the terminal vertex
        else if label[len(label)-1] == particle:
            move_to = position[1]

        else:  # Otherwise, we have nowhere to go!
            return []

        if move_to is not None:
            try:               # is the vertex an int (unoccupied)?
                _ = position[0] + 1
                copy = zero_cell.copy(immutable=False)
                copy.relabel({position[0]: (position[0], particle)})
                return [copy]
            except TypeError:  # the vertex is a tuple (occuplied)!
                pass


    else:
        raise TypeError("position should be a 2- or 3-tuple")


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
        for particle in label:
            yield get_moves_of_particle(zero_cell, particle, (u, v, label))


def one_cells(zero_cells, logger=default_logger):
    """ Given the 0-cells of a graph, what are the 1-cells? """
    assert all(map(lambda g: not g.is_directed(), zero_cells))

    # We're assuming that the order of orientations is deterministic and based
    # on the graph structure, not random nor based on labels. Thus, each 0-cell
    # should get the same orientation.
    for zero_cell in map(lambda g: next(g.orientations()), zero_cells):
        moves = get_moves_from(zero_cell)
