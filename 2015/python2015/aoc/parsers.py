#!/usr/bin/env python
"""
Parser helpers.

# first_line
from aoc.parsers import first_line
directions = first_line(filename)

# all_lines
from aoc.parsers import all_lines
list_of_strings = all_lines(filename)

"""
from typing import List


def first_line(filename: str) -> str:
    """ Given a filename, returns the first line of a file. """
    with open(filename) as file:
        return file.readline().strip()


def all_lines(filename: str) -> List[str]:
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]
