# -*- coding: utf-8 -*-
import pytest
from homology.abrams_y import the_complex
from homology.elementary_collapses import collapse_all

from homology.benchmarks.memoize import memoize
from sage.interfaces.chomp import have_chomp
assert have_chomp() is True

NS = [2, 3]


@memoize
def the_complex_(n, collapsed):
    comp = the_complex(n)
    return collapse_all(comp) if collapsed else comp


@pytest.mark.benchmark(group="construction")
@pytest.mark.parametrize("n", NS)
def test_construction(benchmark, n):
    benchmark(the_complex, n)


@pytest.mark.benchmark(group="collapse")
@pytest.mark.parametrize("n", NS)
def test_collapse_n(benchmark, n):
    benchmark(collapse_all, the_complex_(n, False))


@pytest.mark.benchmark(group="homology")
# @pytest.mark.parametrize("dim", [None, (0, 1)])
@pytest.mark.parametrize("algorithm", ["auto", "no_chomp"])
@pytest.mark.parametrize("n", NS)
def test_homology(benchmark, n, algorithm):  #, dim):
    if not (n == 4 and algorithm == "no_chomp"):
        benchmark(the_complex(n, False).homology, dim=dim, algorithm=algorithm)
    else:
        benchmark(lambda x: x is None, None)
