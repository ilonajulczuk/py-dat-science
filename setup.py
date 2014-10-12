#! /usr/bin/env python
import os
from setuptools import setup

def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dat_science",
    version = "0.0.1",
    author = "Justyna Ilczuk",
    author_email = "justyna.ilczuk@gmail.com",
    description = ("Library for testing alternate code paths in refactoring"),
    license = "BSD",
    keywords = "science refactoring experiments",
    url = "https://github.com/atteroTheGreatest/py-dat-science",
    packages=['dat_science'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)

