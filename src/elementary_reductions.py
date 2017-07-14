#!/usr/bin/env python2

from sage.all import *
from cubical_complex import CubicalComplex

def is_proper_face(c1, c2):
    return c1.is_face(c2) and not c1 == c2

def free_faces(cubical_set):
    """ Return the free faces of a cubical complex """
    proper_faces = []
    for cube in cubical_set.maximal_cells():
        proper_faces += cube.faces()

