#!/usr/bin/env python
"""
Parser helpers.

# first_line
from aoc.parsers import first_line
directions = first_line(filename)

"""


def first_line(filename: str) -> str:
    """ Given a filename, returns the first line of a file. """
    with open(filename) as file:
        return file.readline().strip()
