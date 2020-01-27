#!/usr/bin/env python
"""
Advent Of Code 2015 Day 9
https://adventofcode.com/2015/day/9
"""

from itertools import groupby
from aoc.parsers import first_line


def expand(string: str) -> str:
    # if string = "1112", then
    # runs = [ (3, '1'), (1, '2') ]
    runs = [ (len(list(g)), k) for k, g in groupby(string)]

    output = ""
    for (count, last_char) in runs[1:]:
        output += str(count) + last_char
    return output


class Day10:
    """ AoC 2015 Day 10 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 10 part 1 """
        nums = first_line(filename)
        for _ in range(40):
            nums = expand(nums)
        return len(nums)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 10 part 2 """
        nums = first_line(filename)
        for _ in range(50):
            nums = expand(nums)
        return len(nums)
