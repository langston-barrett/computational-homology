#!/usr/bin/env python2

from sage.all import *
import functools
import heapq


def is_proper_face(cube1, cube2):
    """ Is the first cube a proper face of the second?

    Example 2.8 from Kaczynki, Mischaikow, and Mrozek:

        >>> from cubical_complex import Cube
        >>> Q = Cube([[1,2], [1]])     # [1,2] x [1,1]
        >>> P = Cube([[1,2], [1, 2]])  # [1,2] x [1,2]
        >>> is_proper_face(Q, P)
        True

        >>> is_proper_face(Q, Q)
        False

    Reference: Definition 2.7 from Kaczynki, Mischaikow, and Mrozek
    """
    return cube1.is_face(cube2) and not cube1 == cube2


@functools.total_ordering
class HashCompare():
    """ A wrapper object that allows comparison based on hashing

    Examples:

        >>> HashCompare((), None) == HashCompare((), ())
        True

        >>> HashCompare((), None) == HashCompare(5, "")
        False

        >>> HashCompare(3, None) <= HashCompare(5, "")
        True
    """

    def __init__(self, obj, extra_data):
        self.obj = obj
        self.h = hash(obj)
        self.extra = extra_data

    __eq__ = lambda self, other: self.h == other.h
    __lt__ = lambda self, other: self.h < other.h
    __repr__ = lambda self: repr(self.to_tuple())
    to_tuple = lambda self: (self.obj, self.extra)


def free_faces(cubical_set):
    """ Return the free faces of a cubical complex

    Returns:
        A list of tuples of the form (f, c) where f is a free face and c is the
        unique maximal cube of which f is a face.

    A point has no free faces:

        >>> from cubical_complex import Cube, CubicalComplex
        >>> get = lambda x: map(lambda i: i[0], free_faces(CubicalComplex(x)))
        >>> get([([0, 0], [0, 0])])
        []
    """

    # Example 2.62 of [KMM]:
    heap = []
    for cube in cubical_set.maximal_cells():
        heap += [HashCompare(f, cube) for f in cube.faces()]

    heapq.heapify(heap)
    free = []
    is_free = True  # the current cube is, as far as we know, free

    # Get the first cube from the heap. If there's none left, we're done.
    try:
        cube = heapq.heappop(heap)
    except IndexError:
        return free

    while True:
        # Get the next cube. If there's none left, return what we've got.
        try:
            next = heapq.heappop(heap)
        except IndexError:  # cube is the last element of the heap
            return free + ([cube.to_tuple()] if is_free else [])

        # This cube is the proper face of more than one maximal cube
        if cube == next:
            is_free = False

        elif is_free:
            free.append(cube.to_tuple())  # unpack HashCompare object
            is_free = True

        cube = next


def collapse(cubical_complex, free_face, maximal_face):
    """ Collapse maximal_face by free_face

    We make a new cubical complex with all the same faces except maximal_face
    and free_face.

    NB: Really, only the free faces of maximal_faces need to be re-added (as
    the others are faces of other maximal cubes), but the constructor of
    CubicalComplex eliminates unnecessary faces so we don't worry about it
    here.
    """
    assert maximal_face in cubical_complex.maximal_cells()
    assert free_face in maximal_face.faces()

    return CubicalComplex([c for c in cubical_complex if c != maximal_face] +
                          [f for f in maximal_face.faces() if f != free_face])


def collapse_all(cubical_complex):
    """ Perform all elementary collapses possible on a cubical complex

    This implementation is faster than calling collapse many times, because we
    remove all non-maximal faces at once with the constructor in the return
    statement.

        >>> from cubical_complex import Cube, CubicalComplex
        >>> collapse_all(CubicalComplex([Cube([])]))
        Cubical complex with 0 vertices and 1 cube

        >>> collapse_all(CubicalComplex([Cube([[0, 0]])]))
        Cubical complex with 1 vertex and 1 cube

        >>> collapse_all(CubicalComplex([Cube([[0, 0], [0, 1]])]))
        Cubical complex with 1 vertex and 1 cube
    """
    faces = list(cubical_complex.maximal_cells())
    collapsed = []
    for free, cube in free_faces(cubical_complex):
        # Remove the collapsed cube
        try:
            faces.remove(cube)
        except ValueError:
            pass
        # Add its non-free faces back into the complex
        # TODO: this could be made more efficient. They don't need to be
        # re-added if they are not themselves free faces.
        collapsed.append(free)
        faces += [f for f in cube.faces() if f not in collapsed]
    return CubicalComplex(faces)
