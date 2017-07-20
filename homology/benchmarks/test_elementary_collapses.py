import pytest
from homology.abrams_y import the_complex
from homology.cubical_complex import CubicalComplex
from homology.elementary_collapses import collapse_all

C2Y = the_complex(3)
C3Y = the_complex(3)

# C4Y = the_complex(4, maximality_check=False)
# C4YC = collapse_all(the_complex(4, maximality_check=False))


def test_have_chomp():
    from sage.interfaces.chomp import have_chomp
    assert have_chomp() == True


def mark(grp, f, *args, **kwargs):
    @pytest.mark.benchmark(group=grp)
    def g(benchmark):
        benchmark(f, *args, **kwargs)
    return g


test_C2Y = mark("construction", the_complex, 2)
test_C3Y = mark("construction", the_complex, 3)
test_C2Y_no_chk = mark(
    "construction", the_complex, 2, maximality_check=False)
test_C3Y_no_chk = mark(
    "construction", the_complex, 3, maximality_check=False)
test_C4Y_no_chk = mark(
    "construction", the_complex, 4, maximality_check=False)

test_bench_C2Y = mark("homology", C2Y.homology)
test_bench_C3Y = mark("homology", C3Y.homology)
# test_bench_C4Y = mark(C4Y.homology)

test_bench_C2Y_chomp = mark("homology", C2Y.homology, algorithm="chomp")
test_bench_C3Y_chomp = mark("homology", C3Y.homology, algorithm="chomp")
# test_bench_C4Y_chomp = mark(C4Y.homology, algorithm="chomp")
