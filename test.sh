#!/usr/bin/env bash
set -e

export PYTHONPATH=$PYTHONPATH:$PWD

if ! type -p sage &> /dev/null; then
  sudo docker build --quiet -t computational-homology .
  sudo docker run --rm \
      -v $PWD:/home/sage \
      -t computational-homology \
      ./test.sh
  exit
fi

sage --python setup.py test |& tee test_log
