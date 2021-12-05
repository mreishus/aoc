#!/usr/bin/env python
"""
Advent Of Code 2021 Day 05
https://adventofcode.com/2021/day/5
"""
import re
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


PARSER = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


def parse_line(line):
    (a, b, c, d) = map(int, re.search(PARSER, line).groups())
    return (a, b, c, d)


def steps(a, b):
    """
    steps(5, 9) = 5, 6, 7, 8, 9
    steps(9, 5) = 9, 8, 7, 6, 5
    """

    if b > a:
        return range(a, b + 1)
    elif b < a:
        return range(a, b - 1, -1)
    raise ValueError


def get_line_coords(x1, y1, x2, y2, use_45):
    if x1 == x2:
        for y in steps(y1, y2):
            yield (x1, y)
    elif y1 == y2:
        for x in steps(x1, x2):
            yield (x, y1)
    elif use_45:
        for (x, y) in zip(steps(x1, x2), steps(y1, y2)):
            yield (x, y)


def calculate_overlaps(data, use_diagonal):
    grid = defaultdict(int)
    seen_double = set()

    for (x1, y1, x2, y2) in data:
        for (x, y) in get_line_coords(x1, y1, x2, y2, use_diagonal):
            grid[x, y] += 1
            if grid[x, y] > 1:
                seen_double.add((x, y))

    return len(seen_double)


class Day05:
    """ AoC 2021 Day 05 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 05 part 1 """
        data = parse(filename)
        return calculate_overlaps(data, False)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 05 part 2 """
        data = parse(filename)
        return calculate_overlaps(data, True)
