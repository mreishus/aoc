#!/usr/bin/env python
"""
Advent Of Code 2015 Day 9
https://adventofcode.com/2015/day/9
"""

from aoc.parsers import first_line

def expand(string: str) -> str:
    last_char = None
    count = 0
    runs = []
    for char in string:
        if char != last_char:
            runs.append( (count, last_char) )
            count = 1
            last_char = char
            pass
        else:
            count += 1
    runs.append( (count, last_char) )

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
        for i in range(40):
            nums = expand(nums)
        return len(nums)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 10 part 2 """
        nums = first_line(filename)
        for i in range(50):
            nums = expand(nums)
        return len(nums)
