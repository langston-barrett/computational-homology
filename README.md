# Computational Homology

This project holds some code related
to research I'm doing with [Prof. Safia Chetteh](http://people.reed.edu/~safia/)
on the homology of the configuration spaces of graphs.

## Installation

This project has no development dependencies, but some tools I find useful are
in `shell.nix`. You can use the [Nix package manager](https://nixos.org/nix/) to
handle these.

Since Sage is a pain to install manually, the build, test, and run dependencies
are handled via [Docker](https://www.docker.com/). 

## Testing

Testing can be performed using the pre-made script:

```bash
bash test.sh
```

First, the script checks to see if it's running inside Docker, and re-runs
itself inside a container if not. The main command is this:
```
sage --python setup.py test |& tee test.log
```
The tests are run using [pytest](https://docs.pytest.org/en/latest/). Many are written using simple assertions, but I also used the 
[Hypothesis](https://docs.pytest.org/en/latest/) to write property-based tests
(i.e. tests that run on random inputs and assert properties that all outputs
should hold).

## Code Layout

These are the completed modules:

 * `abrams_y.py`: Constructs a cubical complex based on the Abrams model of the
   configuration space.
 * `cubical_complex`: A copy of Sage's `cubical_complex` module with minor
   modifications.
 * `elementary_collapses`: This module
   implements
   [elementary collapses](https://en.wikipedia.org/wiki/Collapse_(topology)) of
   Sage's cubical complexes. It uses a somewhat odd internal data structure for
   faster operations, which is documented thoroughly within. 
 * `swiatkowski`: This module contains the building blocks for developing code
   to take as input a generic graph and give as output the cubical complex that
   arises from
   the
   [Świątkowski model](https://userpage.fu-berlin.de/luetge/pdfs/masters-thesis-luetgehetmann.pdf).

     - `swiatkowski.zero_cells`: Return a list of all possible configurations of
       n points on a graph in the Świątkowski model.

 * `useful_but_unused`: Bits of code that I wrote and work well, but aren't
   currently necessary for other modules.
 
## Results

Elementary collapses don't speed up the calculation of homology of cubical
complexes significantly. In part, this is because a cube of dimension _d_ has
2^d vertices, and so might have to be collapsed more than 2^d times.
Furthermore, the [CHomP](https://github.com/shaunharker/CHomP) library, when
available in your Sage installation, already performs more advanced collapses
using concepts
from
[discrete Morse theory](https://en.wikipedia.org/wiki/Discrete_Morse_theory).

I wish we had more time to develop the Świątkowski model code, which would
output a cubical complex of significantly lower dimension (bounded above by _n_
and the number of vertices of degree 3 or more).

## References

 * Kaczynski T, Mischaikow K, Mrozek M. Computational Homology. Springer Science & Business Media; 2006.
 * Lütgehetmann, Daniel. Master's Thesis. Freie Universität Berlin.

I also looked at a lot of work
of [Safia Chetteh's](https://people.reed.edu/~safia/)
and [Robert Ghrist](https://www.math.upenn.edu/~ghrist/).
