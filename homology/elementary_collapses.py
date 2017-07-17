#!/usr/bin/env python2

from sage.all import *


def is_proper_face(cube1, cube2):
    """ Is the first cube a proper face of the second?

    Example 2.8 from Kaczynki, Mischaikow, and Mrozek:

        >>> from homology.cubical_complex import Cube
        >>> Q = Cube([[1,2], [1]])     # [1,2] x [1,1]
        >>> P = Cube([[1,2], [1, 2]])  # [1,2] x [1,2]
        >>> is_proper_face(Q, P)
        True

        >>> is_proper_face(Q, Q)
        False

    Reference: Definition 2.7 from Kaczynki, Mischaikow, and Mrozek
    """
    return cube1.is_face(cube2) and not cube1 == cube2


def free_faces(cubical_set):
    """ Return the free faces of a cubical complex

    Returns:
        A list of tuples of the form (f, c) where f is a free face and c is the
        unique maximal cube of which f is a face.

    A point has no free faces:

        >>> from homology.cubical_complex import Cube, CubicalComplex
        >>> get = lambda x: map(lambda i: i[0], free_faces(CubicalComplex(x)))
        >>> get([([0, 0], [0, 0])])
        []
    """
    table = dict()
    for cube in cubical_set.maximal_cells():
        for face in cube.faces():
            try:
                table[face].append(cube)
            except KeyError:
                table[face] = [cube]

    # Only return the free faces, i.e. those that are face of a single cube
    return [(face, cubes[0]) for face, cubes in table.items()
            if len(cubes) == 1]


def collapse(cubical_complex, free_face, maximal_face, maximality_check=True):
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

    return CubicalComplex(
        [c for c in cubical_complex if c != maximal_face] +
        [f for f in maximal_face.faces() if f != free_face],
        maximality_check=maximality_check)


def collapse_all(cubical_complex, maximality_check=True):
    """ Perform all elementary collapses possible on a cubical complex

    This implementation is faster than calling collapse many times, because we
    remove all non-maximal faces at once with the constructor in the return
    statement.

        >>> from homology.cubical_complex import Cube, CubicalComplex
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
    return CubicalComplex(faces, maximality_check=maximality_check)
