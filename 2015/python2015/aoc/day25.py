#!/usr/bin/env python
"""
Advent Of Code 2015 Day 25
https://adventofcode.com/2015/day/25
"""

from typing import List
from aoc.parsers import all_lines
from itertools import combinations
from functools import reduce
from operator import mul


def part1(target_x: int, target_y: int) -> int:
    x = 1
    y = 1
    val = 20151125

    while y != target_y or x != target_x:
        if y == 1:
            y = x + 1
            x = 1
        else:
            x += 1
            y -= 1
        val = (val * 252533) % 33554393
    return val


class Day25:
    """ AoC 2015 Day 25 """

    @staticmethod
    def part1(_filename: str) -> int:
        """ Given a filename, solve 2015 day 25 part 1 """
        # Too lazy to parse: These come from input.txt
        target_x = 3075
        target_y = 2981
        return part1(target_x, target_y)
