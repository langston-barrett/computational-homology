#!/usr/bin/env python2
# -*- mode: python -*-

# from sage.all import *
from homology import abrams_y
import pytest

# For debugging functions that aren't working
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler(filename="debug.log", mode="w"))


def test_lookup():
    assert [(0, 0, 0)] == abrams_y.lookup(1)
    assert [(0, 1, 0), (0, 0, 0), (1, 0, 0), (0, 0, 1)] == abrams_y.lookup(2)


def test_generate_tree():
    with pytest.raises(AssertionError):
        abrams_y.generate_tree(0)

    assert ([1, 1], [], []) == abrams_y.generate_tree(1)
    assert ([1], [2, 3], [], []) == abrams_y.generate_tree(2)

# TODO: this fails!
# def test_maximality_granular():
#     for i in [2, 3]:
#         not_checked = abrams_y.the_complex(i, maximality_check=False)
#         cells = not_checked.maximal_cells()
#         for cell in cells:
#             for other_cell in cells:
#                 if cell != other_cell:
#                     try:
#                         assert not cell.is_face(other_cell)
#                     except AssertionError as e:
#                         print("*"*80)
#                         print(cell)
#                         print(other_cell)
#                         raise e

# TODO: this fails!
# def test_maximality():
#     """ When does this currently fail?

#      * The downstream cubes of point configurations in which one point is at
#        the end of a leg are faces of the ones preceeding them
#      * The downstream cubes of (1, 2, 3) are faces of those of (0, 2, 3) - why?
#     """
#     # for i in [2, 3, 4]:  # takes forever
#     for i in [2, 3]:
#         checked = abrams_y.the_complex(i, maximality_check=True)
#         not_checked = abrams_y.the_complex(i, maximality_check=False, logger=logger)
#         assert checked == not_checked


def test_homology():
    assert "{0: 0, 1: Z}" == str(abrams_y.the_complex(2).homology())
    assert "{0: 0, 1: Z^13, 2: 0, 3: 0}" == str(
        abrams_y.the_complex(3).homology())
