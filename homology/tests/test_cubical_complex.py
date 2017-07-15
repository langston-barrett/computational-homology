#!/usr/bin/env python2
# -*- mode: python -*-

from sage.all import *
from homology import cubical_complex
from homology.cubical_complex import Cube, CubicalComplex


# TODO:
# def test_maximal_cubes(self):
#     f = CubicalComplex.maximal_cubes
#     self.assertEqual([Cube([])], f([Cube([])]))
#     self.assertEqual([Cube([[0,0]])], f([Cube([[0,0]])]))
#     self.assertEqual([Cube([[0,0], [0,1]])], f([Cube([[0,0], [0,1]])]))
#     self.assertEqual([Cube([[0,0], [0,1]])],
#                      f(map(Cube, [[[0,0], [0,1]], [[0,0]], [[0,1]]])))
