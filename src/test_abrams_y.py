#!/usr/bin/env python2
# -*- mode: python -*-

from sage.all import *
import doctest
import unittest

import abrams_y


class Tests(unittest.TestCase):
    def test_lookup(self):
        self.assertEqual([(0, 0, 0)], abrams_y.lookup(1))
        self.assertEqual([(0, 1, 0), (0, 0, 0), (1, 0, 0), (0, 0, 1)],
                         abrams_y.lookup(2))

    def test_generate_tree(self):
        self.assertRaises(AssertionError, abrams_y.generate_tree, 0)

        self.assertEqual(([1, 1], [], []), abrams_y.generate_tree(1))
        self.assertEqual(([1], [2, 3], [], []), abrams_y.generate_tree(2))
        # self.assertEqual(([1], [2, 3], [], []), abrams_y.generate_tree(3))

    def test_homology(self):
        self.assertEqual("{0: 0, 1: Z}",
                         str(abrams_y.the_complex(2).homology()))
        self.assertEqual("{0: 0, 1: Z^13, 2: 0, 3: 0}",
                         str(abrams_y.the_complex(3).homology()))


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(Tests))
    suite.addTests(doctest.DocTestSuite(abrams_y))
    return suite


if __name__ == "__main__":
    unittest.main()
