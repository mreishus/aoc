#!/usr/bin/env python
"""
Advent Of Code 2015 Day 12
https://adventofcode.com/2015/day/12
"""

import json
from aoc.parsers import first_line


def total_nums(data) -> int:
    if isinstance(data, dict):
        total = 0
        for (_, v) in data.items():
            total += total_nums(v)
        return total
    if isinstance(data, list):
        return sum(total_nums(x) for x in data)
    if isinstance(data, int):
        return data
    return 0


def total_nums_no_red(data) -> int:
    if isinstance(data, dict):
        ## Special case: Dicts containing red as a value return 0
        has_red = any(val == "red" for val in data.values())
        if has_red:
            return 0

        total = 0
        for (_, v) in data.items():
            total += total_nums_no_red(v)
        return total
    if isinstance(data, list):
        return sum(total_nums_no_red(x) for x in data)
    if isinstance(data, int):
        return data
    return 0


class Day12:
    """ AoC 2015 Day 12 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 12 part 1 """
        data = first_line(filename)
        data = json.loads(data)
        return total_nums(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 12 part 2 """
        data = first_line(filename)
        data = json.loads(data)
        return total_nums_no_red(data)
