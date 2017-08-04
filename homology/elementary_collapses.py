#!/usr/bin/env python2
"""
TODO document the dict format

 * n is the number of (maximal) cubes in the complex
 * d is their maximal dimension

Thus, face_d has O(2d*n)=O(d*n) keys, since each cube of dimension d has 2d
faces (see Wikipedia:Hypercube#Elements).
"""

from sage.all import *
from functools import reduce

import random  # TODO: delete me
import logging

# Logging configuration: by default, produce no output
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def add_maximal(face_d, cube):
    """ Add a newly maximal cube by introducing its faces as keys

    We add cubes with no faces (the empty cube, vertices) to the special key
    None.

    Runtime: O(d)
        Appends one item to a list for each face of "cube".

     * An empty cube has no faces to use as keys:

        >>> from homology.cubical_complex import Cube
        >>> add_maximal(dict(), Cube([]))
        {None: []}

     * A point also has no faces, but we add it specially TODO:

        >>> add_maximal(dict(), Cube([[0, 0]]))
        {None: [[0,0]]}

     * A line has two faces, and if we add the faces from another line that it
       intersects at a vertex, we have only three maximal faces (vertices):

        >>> d = add_maximal(dict(), Cube([[0, 0], [0, 1]]))
        >>> d
        {[0,0] x [0,0]: [[0,0] x [0,1]], [0,0] x [1,1]: [[0,0] x [0,1]]}
        >>> len(add_maximal(d, Cube([[0, 1], [0, 0]])))
        3

       The picture is like this:

         [0,0] x [1,1] ->  *
                           |
         [0,0] x [0,0] ->  *--*

     * A cube has six faces:

        >>> len(add_maximal(dict(), Cube([[0, 1], [0, 1], [0, 1]])))
        6
    """
    # assert that it's not the face of some other cube
    assert face_d.get(cube, None) is None

    # If it's a point, add it to the key None
    faces = cube.faces()
    faces = [None] if faces == [] else faces

    for face in faces:
        try:
            face_d[face].append(cube)
        except KeyError:
            face_d[face] = [cube]

    return face_d


def face_dict(maximal_cells):
    """ Returns a dictionary which has the primary faces of the maximal cubes
    of the complex as keys and the maximal cubes of which they are faces as
    values.

    Runtime: O(dn)
        Runs add_maximal for each cube in maximal_cells.


     * Empty dicts:
        >>> from homology.cubical_complex import Cube
        >>> face_dict([Cube([])])
        {None: []}
        >>> face_dict([Cube([[0, 0]])])
        {None: [[0,0]]}


     * A more interesting example:

        >>> face_dict([Cube([[0, 0], [0, 1]]), Cube([[0, 1], [0, 0]])])
        {[1,1] x [0,0]: [[0,1] x [0,0]],
         [0,0] x [0,0]: [[0,0] x [0,1], [0,1] x [0,0]],
         [0,0] x [1,1]: [[0,0] x [0,1]]}

       The picture is like this:

         [0,0] x [1,1] ->  *
                           |
         [0,0] x [0,0] ->  *--*
    """
    try:  # See if it's a cubical complex
        maximal_cells = set(maximal_cells.maximal_cells())
    except AttributeError:
        pass
    return reduce(lambda d, cube: add_maximal(d, cube), maximal_cells, dict())


def collapse(face_d, free_face, logger=logger):
    """ Collapse a single free face, and update face_d accordingly.

    The key realization of this algorithm is that collapsing is a local
    phenomenon: only faces of the collapsed maximal cell can become new
    maximal or free faces.

    NB: This only works if free_face is a free face of maximal dimension, i.e.
    there are no free faces of higher dimension.

    Runtime: O(d^2)
        In the worst case, runs add_maximal (O(d)) for each face of the maximal
        cube which free_face is a face of.

    Examples:

     * Collapsing the interval:

        >>> from homology.cubical_complex import Cube, CubicalComplex
        >>> I = Cube([(0, 1), (0, 0)])
        >>> collapse(face_dict(CubicalComplex([I])), Cube([(0,0), (0,0)]))
        {None: [[1,1] x [0,0]]}

     * Collapsing a maximal 2-cell by a free 1-cell:

        >>> cube1 = Cube([(0, 1), (0, 1)])
        >>> cube2 = Cube([(1, 2), (0, 1)])
        >>> c2 = CubicalComplex([cube1, cube2])
        >>> d = face_dict(c2)
        >>> d # we see that [2,2] x [0,1] is free
        {[0,0] x [0,1]: [[0,1] x [0,1]], ...,
         [2,2] x [0,1]: [[1,2] x [0,1]], ...,
         [0,1] x [0,0]: [[0,1] x [0,1]]}
        >>> free = Cube([[2, 2], [0, 1]])
        >>> collapsed = collapse(d, free)
        >>> collapsed.get(free, False) # it's removed from the dict
        False
        >>> collapsed[Cube([[2, 2], [0, 0]])] # and new faces are added
        [[1,2] x [0,0]]

       This is the corresponding picture:

        *--*--*                                           *--*--*
        |xx|xx| --- collapse via RHS ([2,2] x [0,1]) ---> |xx|
        *--*--*                                           *--*--*

      *

    """
    # assert that the face is indeed free
    assert len(face_d[free_face]) == 1
    # assert that the free face is indeed a primary face of this maximal cell
    assert free_face in face_d[free_face][0].faces()

    # the unique maximal cell which this free face is a face of
    remove = face_d[free_face][0]

    logger.debug("Collapsing {} by {}".format(remove, free_face))

    # Remove the free face
    face_d.pop(free_face)

    # Remove the maximal cell and add all of the other faces of "remove" back
    # to the complex. We only need to add the faces that are not already
    # primary faces of other maximal cells.
    for face in [face for face in remove.faces() if face != free_face]:
        # All of its faces are primary faces of a maximal cube, so they're
        # already in the dict.
        # We need to remove "remove" from the list of cubes they're faces of.
        face_d[face].remove(remove)

        # If it's now maximal, then add it as a maximal face
        if face_d[face] == []:
            face_d.pop(face)
            face_d = add_maximal(face_d, face)
        # Otherwise, it might now be free! Yay!

        # We collapsed it
    assert face_d.get(free_face, None) is None

    logger.debug("After collapsing: {}".format(
        face_dict_to_complex(face_d).maximal_cells()))

    return face_d


def face_dict_to_complex(face_d, maximality_check=False):
    """ Convert a dictionary of free faces back into a CubicalComplex

    The maximality check _should_ be extraneous, and we test that using
    Hypothesis. Just to be careful, we leave it in as an option.

    Runtime: less than O(n)

    Examples: TODO
    """
    maximal = set()
    for face, maximal_cubes in face_d.items():
        maximal.update(maximal_cubes)

    return CubicalComplex(maximal, maximality_check=maximality_check)


def get_free_face(face_d, logger=logger):
    """ Get a single free face of maximal dimension from face_d

    Runtime:
        O(d*n): loops through the keys of face_d, of which there are 2d*n

    Returns:
        Either a key of face_d, or None if there are no faces in face_d.

        >>> get_free_face(dict())
        False

        >>> from homology.cubical_complex import Cube, CubicalComplex
        >>> get_free_face(face_dict(CubicalComplex([Cube([(0,1)])])))
        [1,1]

    TODO: tests and examples
    """
    maximal_dimension = -1
    maximal_free = False
    for face, cubes in face_d.items():
        if face is not None and len(cubes) == 1:
            new_dimension = face.dimension()
            logger.debug("Dimension of {} is {}".format(face, new_dimension))
            if new_dimension > maximal_dimension:
                logger.debug("HERE")
                maximal_dimension = new_dimension
                maximal_free = face

    logger.debug("Returning free face {}".format(maximal_free))
    return maximal_free


def collapse_all(cubical_complex, maximality_check=True, logger=logger):
    """ Perform all elementary collapses possible on a cubical complex

    Runtime: O(d^2n)

     * You can't collapse a point:
        >>> from homology.cubical_complex import Cube, CubicalComplex
        >>> pt = CubicalComplex([Cube([(0, 0)])])
        >>> collapse_all(pt).maximal_cells()
        {[0,0]}

     * Intervals:

        >>> I = Cube([(0, 1), (0, 0)])
        >>> collapse_all(CubicalComplex([I])).maximal_cells()
        {[1,1] x [0,0]}

        >>> I2 = Cube([(0, 1), (0, 1)])
        >>> collapse_all(CubicalComplex([I2])).maximal_cells()
        {[0,0] x [0,0]}

     * None of the faces of the square are free:

        >>> SQUARE = CubicalComplex([
        ...     Cube([(0, 1), (0, 0)]), Cube([(0, 1), (1, 1)]),
        ...     Cube([(0, 0), (0, 1)]), Cube([(1, 1), (0, 1)])
        ... ])
        ...
        >>> assert SQUARE == collapse_all(SQUARE)

     * It removes _a lot_ of cubes:

        >>> from homology.abrams_y import the_complex
        >>> c = the_complex(3)
        >>> c
        Cubical complex with 210 vertices and 756 cubes

        >>> collapse_all(c)
        Cubical complex with 148 vertices and 308 cubes

    """
    logger.debug("*** Collapsing all in {}".format(cubical_complex))
    face_set = set(cubical_complex.maximal_cells())
    face_d = face_dict(face_set)
    free = get_free_face(face_d)
    while free is not False:  # Up to 2^n loops, if acyclic?
        face_d = collapse(face_d, free, logger=logger)
        free = get_free_face(face_d) # O(dn)

    return face_dict_to_complex(face_d, maximality_check=maximality_check)
