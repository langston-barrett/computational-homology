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


def get_moves_of_vertex(zero_cell, vertex):
    """ Get a list of moves that this particle can make
    """


def get_moves_from(zero_cell):
    """ Get all possible moves (1-cells) emanating from this configuration """
    f = functools.partial(get_moves_of_vertex, zero_cell)
    return itertools.imap(f, zero_cell.vertices())


def one_cells(zero_cells, logger=default_logger):
    """ Given the 0-cells of a graph, what are the 1-cells? """

    for zero_cell in zero_cells:
        moves = get_moves_from(zero_cell)
