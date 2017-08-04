#!/usr/bin/env python
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="computational-homology",
    version="0.1.0",
    long_description=long_description,
    url="https://github.com/siddharthist/computational-homology",
    author="Langston Barrett (@siddharthist)",
    license="MPL-2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Mathematicians",
        "Programming Language :: Python :: 2",
    ],

    keywords="homology cubical complex",
    packages=find_packages(exclude=["docs", "benchmarks", "tests"])
)
