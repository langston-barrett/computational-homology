#!/usr/bin/env bash

sudo docker run \
     -v $PWD:/home/sage \
     -it sagemath/sagemath \
     sage -python src/test_cubical_complex.py
     # sage -python src/test_abrams_y.py
