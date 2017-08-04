# -*- coding: utf-8 -*-
import hypothesis
import functools

from homology.abrams_y import the_complex
from homology.elementary_collapses import add_maximal, face_dict, face_dict_to_complex, get_free_face, collapse_all
from homology.cubical_complex import Cube, CubicalComplex
from homology.tests.cubical_hypothesis import random_cube, random_complex, random_interval

# For debugging functions that aren't working
# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.FileHandler(filename="debug.log", mode="w"))

# Increase these for more thorough, but longer tests
MAX_EMBED = 20
MAX_CUBES = 25
given_complex = functools.partial(
    random_complex,
    max_embed=MAX_EMBED,
    max_cubes=MAX_CUBES,
    maximality_check=True)


@hypothesis.given(random_cube(min_dimension=1, max_embed=5))
def test_add_maximal(cube):
    assert len(add_maximal(dict(), cube)) > 0


@hypothesis.given(
    random_complex(
        max_embed=5, max_cubes=10, maximality_check=True))
def test_face_dict(complex):
    """\
     1. None of the primary faces of maximal cubes are themselves maximal
     2. All keys are actually faces of their values
    """
    face_set = set(complex.maximal_cells())
    face_d = face_dict(face_set)
    for face, cubes in face_d.items():
        assert face not in face_set  # 1

        for cube in cubes:
            if face is not None:
                assert face in cube.faces()  # 2


@hypothesis.given(random_interval(degenerate=True))
def test_collapse_degenerate_interval(interval):
    """ Degenerate intervals can't be collapsed """
    complex = CubicalComplex([Cube([interval])])
    assert complex == collapse_all(complex)


@hypothesis.given(given_complex())
def test_face_d_to_complex(complex):
    """ \
    1. Test that the maximality check is extraneous
    2. Test that the representation as and conversion of complexes to/from
       face dictionaries is faithful
    """
    d = face_dict(complex)
    assert face_dict_to_complex(d) == face_dict_to_complex(
        d, maximality_check=False)
    assert complex == face_dict_to_complex(d)


def compare_homology(c1, c2):
    # C1 should be the smaller
    if len(c1) > len(c2):
        c1, c2 = c2, c1

    # The ones they share should be identical
    for k, v in c1.items():
        assert c2[k] == v

    # All other groups should be trivial
    # for k, v in c2.items():
    #     if not c1.get(k, False):
    #         assert v.order() == 1


@hypothesis.given(random_cube(max_embed=MAX_EMBED, min_dimension=1))
def test_get_free_face(cube):
    """ All elementary cubes have free faces """
    assert get_free_face(
        face_dict(CubicalComplex([cube]))) is not False


# TODO: this is slow
# @hypothesis.given(given_complex())
@hypothesis.given(
    random_complex(
        max_embed=5, max_cubes=20, maximality_check=True))
@hypothesis.example(CubicalComplex([Cube([(0, 1), (0, 1), (0, 1)])]))  # I^3
def test_collapse_all(cubical_complex):
    collapsed = collapse_all(cubical_complex)

    # This doesn't belong here, but it's efficient, so ¯\_(ツ)_/¯
    assert get_free_face(face_dict(collapsed)) is False

    compare_homology(
        cubical_complex.homology(algorithm="no_chomp"),
        collapsed.homology(algorithm="no_chomp"))


def test_collapse_all_the_complex():
    for i in [2, 3]:
        comp = the_complex(i)
        compare_homology(
            comp.homology(algorithm="auto"),
            collapse_all(comp).homology(algorithm="auto"))
