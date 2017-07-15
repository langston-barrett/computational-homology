#!/usr/bin/env python2
# -*- mode: python -*-

from sage.all import *
from homology import elementary_collapses
from homology.elementary_collapses import free_faces, collapse_all
from homology.cubical_complex import Cube, CubicalComplex, cubical_complexes


def random_cube():
    pass


def random_complex():
    pass


def test_free_faces():
    get = lambda x: map(lambda i: i[0], free_faces(CubicalComplex(x)))
    # A line has two free faces
    assert [Cube([[0, 0], [0, 0]]), Cube([[0, 0], [1, 1]])] == get(
        [([0, 0], [0, 1])])

    # A cube has six faces
    assert 6 == len(get([([0, 1], [0, 1], [0, 1])]))


def test_collapse():
    # ([0, 0], [1, 1])  ->  *  --collapse-> *
    # ([0, 0], [0, 1])  ->  |
    # ([0, 0], [0, 0])  ->  *
    line = ([0, 0], [0, 1])
    assert CubicalComplex(
        [([0, 0], [1, 1])]) == collapse_all(CubicalComplex([line]))


from homology.abrams_y import the_complex

def test_benchmark_uncollapsed(benchmark):
    c = the_complex(4, maximality_check=False)
    benchmark(c.homology)

def test_benchmark_collapsed(benchmark):
    c_reduced = collapse_all(the_complex(4, maximality_check=False))
    benchmark(c_reduced.homology)
