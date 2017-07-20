import hypothesis
from hypothesis import strategies
from homology.cubical_complex import Cube, CubicalComplex
""" Hypothesis strategies for generating cubes and cubical complexes """


@strategies.composite
def random_interval(draw, degenerate=None):
    if degenerate is None:
        degenerate = draw(strategies.booleans())
    first = draw(strategies.integers())
    if degenerate:
        return (first, first)
    return (first, first + 1)


@strategies.composite
def random_cube(draw, embed=None, max_embed=100, min_dimension=0):
    if embed is None:
        embed = draw(strategies.integers(min_value=0, max_value=max_embed))

    intervals = [draw(random_interval(degenerate=False))
                 for _ in range(min_dimension)]
    intervals += [draw(random_interval())
                  for _ in range(embed - min_dimension)]
    return Cube(intervals)


@strategies.composite
def random_complex(draw,
                   embed=None,
                   max_embed=100,
                   cubes=None,
                   max_cubes=100,
                   maximality_check=False):
    if cubes is None:
        cubes = draw(strategies.integers(min_value=0, max_value=max_cubes))

    return CubicalComplex(
        [draw(random_cube(
            embed=embed, max_embed=max_embed)) for _ in range(cubes)],
        maximality_check=maximality_check)
