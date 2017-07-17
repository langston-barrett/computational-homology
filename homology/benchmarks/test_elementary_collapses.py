from homology.elementary_collapses import collapse_all
from homology.abrams_y import the_complex


C2Y = the_complex(3)
C2YC = collapse_all(the_complex(3))
C3Y = the_complex(3)
C3YC = collapse_all(the_complex(3))
C4Y = the_complex(4, maximality_check=False)
# C4YC = collapse_all(the_complex(4, maximality_check=False))


def test_have_chomp():
    from sage.interfaces.chomp import have_chomp
    assert have_chomp() == True


def mark(f, *args, **kwargs):
    return lambda benchmark: benchmark(f, *args, **kwargs)


# Construction
test_b_construct_C2Y = mark(the_complex, 2)
test_b_construct_C3Y = mark(the_complex, 3)
test_b_construct_C2Y_no_maximality_check = mark(the_complex, 2, maximality_check=False)
test_b_construct_C3Y_no_maximality_check = mark(the_complex, 3, maximality_check=False)
test_b_construct_C4Y_no_maximality_check = mark(the_complex, 4, maximality_check=False)


test_bench_C2Y = mark(C2Y.homology)
test_bench_C2YC = mark(C2YC.homology)
test_bench_C3Y = mark(C3Y.homology)
test_bench_C3YC = mark(C3YC.homology)
test_bench_C4Y = mark(C4Y.homology)
# test_bench_C4YC = mark(C4YC.homology)

test_bench_C2Y_chomp = mark(C2Y.homology, algorithm="chomp")
test_bench_C2YC_chomp = mark(C2YC.homology, algorithm="chomp")
test_bench_C3Y_chomp = mark(C3Y.homology, algorithm="chomp")
test_bench_C3YC_chomp = mark(C3YC.homology, algorithm="chomp")
test_bench_C4Y_chomp = mark(C4Y.homology, algorithm="chomp")
