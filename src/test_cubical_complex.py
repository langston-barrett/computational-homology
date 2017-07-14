#!/usr/bin/env python2
# -*- mode: python -*-

from sage.all import *
import doctest
import unittest

import cubical_complex
from cubical_complex import Cube, CubicalComplex


class Tests(unittest.TestCase):
    pass

    # TODO:
    # def test_maximal_cubes(self):
    #     f = CubicalComplex.maximal_cubes
    #     self.assertEqual([Cube([])], f([Cube([])]))
    #     self.assertEqual([Cube([[0,0]])], f([Cube([[0,0]])]))
    #     self.assertEqual([Cube([[0,0], [0,1]])], f([Cube([[0,0], [0,1]])]))
    #     self.assertEqual([Cube([[0,0], [0,1]])],
    #                      f(map(Cube, [[[0,0], [0,1]], [[0,0]], [[0,1]]])))


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(Tests))
    suite.addTests(
        doctest.DocTestSuite(
            cubical_complex, optionflags=doctest.NORMALIZE_WHITESPACE))
    return suite


if __name__ == "__main__":
    unittest.main()
