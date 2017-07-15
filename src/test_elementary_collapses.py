#!/usr/bin/env python2
# -*- mode: python -*-

from sage.all import *
import doctest
import unittest

import elementary_collapses
from elementary_collapses import free_faces, collapse_all
from cubical_complex import Cube, CubicalComplex, cubical_complexes

def random_cube():
    pass

def random_complex():
    pass


class Tests(unittest.TestCase):
    def test_free_faces(self):
        get = lambda x: map(lambda i: i[0], free_faces(CubicalComplex(x)))
        # A line has two free faces
        self.assertEqual([Cube([[0, 0], [0, 0]]), Cube([[0, 0], [1, 1]])],
                         get([([0, 0], [0, 1])]))

        # A cube has six faces
        self.assertEqual(6, len(get([([0, 1], [0, 1], [0, 1])])))

    def test_collapse(self):
        # ([0, 0], [1, 1])  ->  *  --collapse-> *
        # ([0, 0], [0, 1])  ->  |
        # ([0, 0], [0, 0])  ->  *
        line = ([0, 0], [0, 1])
        self.assertEqual(
            CubicalComplex([([0, 0], [1, 1])]),
            collapse_all(CubicalComplex([line])))


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(Tests))
    suite.addTests(doctest.DocTestSuite(elementary_collapses))
    return suite


if __name__ == "__main__":
    unittest.main()
