#!/usr/bin/env python2
# -*- mode: python -*-

from sage.all import *
import doctest
import unittest

import cubical_complex
from cubical_complex import Cube, CubicalComplex


class Tests(unittest.TestCase):
    def test_maximal_cubes(self):
        TESTS = [
            # ([], [Cube([])]),
            # ([], [Cube([[0,0], [0,1]])]),
        ]
        for test in TESTS:
            self.assertEqual(test[0], CubicalComplex.maximal_cubes(test[1]))


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(Tests))
    suite.addTests(
        doctest.DocTestSuite(
            cubical_complex, optionflags=doctest.NORMALIZE_WHITESPACE))
    return suite


if __name__ == "__main__":
    unittest.main()
