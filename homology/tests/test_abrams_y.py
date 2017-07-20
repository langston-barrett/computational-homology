#!/usr/bin/env python2
# -*- mode: python -*-

# from sage.all import *
from homology import abrams_y
import pytest


def test_lookup():
    assert [(0, 0, 0)] == abrams_y.lookup(1)
    assert [(0, 1, 0), (0, 0, 0), (1, 0, 0), (0, 0, 1)] == abrams_y.lookup(2)


def test_generate_tree():
    with pytest.raises(AssertionError):
        abrams_y.generate_tree(0)

    assert ([1, 1], [], []) == abrams_y.generate_tree(1)
    assert ([1], [2, 3], [], []) == abrams_y.generate_tree(2)


def test_homology():
    assert "{0: 0, 1: Z}" == str(abrams_y.the_complex(2).homology())
    assert "{0: 0, 1: Z^13, 2: 0, 3: 0}" == str(
        abrams_y.the_complex(3).homology())
