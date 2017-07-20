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

def all_faces(cube):
    """ Get all the faces of a cube, not just the primary faces

    Runtime:
      O(2^m): A cube of dimension m has 2^m vertices.
      https://en.wikipedia.org/wiki/Hypercube

     * The empty cube has no faces:

        >>> from homology.cubical_complex import Cube
        >>> all_faces(Cube([]))
        set([])

     * A line has two faces, its endpoints:

        >>> all_faces(Cube([[0, 0], [0, 1]]))  # [0, 0] x [0, 1]
        set([[0,0] x [0,0], [0,0] x [1,1]])

     * A square has 8 faces: 4 edges + 4 vertices:

        >>> len(all_faces(Cube([[0, 1], [0, 1]])))  # I^2
        8

     * A cube has 26 faces: 6 sides + 12 edges + 8 vertices:

        >>> len(all_faces(Cube([[0, 1], [0, 1], [0, 1]])))  # I^3
        26
    """
    to_return = set()
    to_return.update(cube.faces())
    for face in cube.faces():
        to_return.update(all_faces(face))
    return to_return

# This test helped debug an error in collapse_all, and revealed the necessity
# of collapsing maximal cubes first.
'''
@hypothesis.given(
    random_complex(
        max_embed=5, max_cubes=15, maximality_check=True))
def test_collapse_single(cubical_complex):
    """ For debugging: keep collapsing, asserting each time that the homology
    doesn't change """
    face_set = set(cubical_complex.maximal_cells())
    face_d = face_dict(face_set)
    free = get_free_face(face_d)
    while free is not None:
        face_d = collapse(face_d, free, logger=logger)
        complex_ = face_dict_to_complex(face_d)

        logger.debug(">>> Comparing homology...")
        logger.debug(">>> Complex 1: {}".format(cubical_complex.maximal_cells()))
        logger.debug(">>> Complex 2: {}".format(complex_.maximal_cells()))
        compare_homology(cubical_complex.homology(), complex_.homology())
        free = get_free_face(face_d)
'''
