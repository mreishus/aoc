#!/usr/bin/env python
"""
Advent Of Code 2021 Day 05
https://adventofcode.com/2021/day/5
"""
import re
from typing import Generator, List
from collections import defaultdict
from itertools import repeat


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


PARSER = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


def parse_line(line: str) -> tuple[int, int, int, int]:
    (a, b, c, d) = map(int, re.search(PARSER, line).groups())
    return (a, b, c, d)


def steps(a: int, b: int) -> range:
    """
    steps(5, 9) = 5, 6, 7, 8, 9
    steps(9, 5) = 9, 8, 7, 6, 5
    """

    if b > a:
        return range(a, b + 1)
    elif b < a:
        return range(a, b - 1, -1)
    raise ValueError


def get_line_coords(
    x1: int, y1: int, x2: int, y2: int, use_45: bool
) -> Generator[tuple[int, int], None, None]:
    if x1 == x2:
        yield from zip(repeat(x1), steps(y1, y2))
    elif y1 == y2:
        yield from zip(steps(x1, x2), repeat(y1))
    elif use_45:
        yield from zip(steps(x1, x2), steps(y1, y2))


def calculate_overlaps(
    data: List[tuple[int, int, int, int]], use_diagonal: bool
) -> int:
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
