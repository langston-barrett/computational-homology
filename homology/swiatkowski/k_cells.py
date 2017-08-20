# -*- coding: utf-8 -*-
"""\
Generate the k-cells, or "moves", of n points on a graph in the Swiatkowski
model.
"""

def one_cells_from_pt(conf, pt):
    """ A list of all 1-cells that arise from moving the given point

    If the point is on a branched vertex, it can move onto any of its adjacent
    edges. If the point is on the end of an edge, it can move to the nearest
    branched vertex. If a point is in the middle of an edge, it cannot move.
    """

def one_cells(conf):
    """ A list of all one cells emanating from a given point
    """


def compatible_cells(conf, cell1, cell2):
    """ Can these cells be combined into higher-dimensional ones? """

def combine_cells():
    """ Given a k-cell and and l-cell, make a (k+l)-cell """


def moves_from(conf):
    """ A list of all moves available from this starting position """


def k_faces(G, zero_cells):
    """ A list of k-faces, which are the elements of the poset P_n^(k)(Γ).

    As explained in Section 2.1 of Lütgehetmann, this poset consists of pairs
    F = (f, f^mov) where f is a 0-cell (configuration) and f^mov is a function

    In the paper, zero cells are represented as certain functions
    f:E ∪ B → Tup_n(n), whereas we represent them as labelings on a graph.
    """
