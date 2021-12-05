#!/usr/bin/env python
"""
Advent Of Code 2021 Day 05
https://adventofcode.com/2021/day/5
"""
from typing import List
import re
from collections import defaultdict

PARSER = re.compile("(\d+),(\d+) -> (\d+),(\d+)")


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    (a, b, c, d) = re.search(PARSER, line).groups()
    return (int(a), int(b), int(c), int(d))


def getrange(a, b):
    if b > a:
        return list(range(a, b + 1))
    elif b < a:
        return list(range(a, b - 1, -1))
    exit("Fail assert")
    return []


class Board:
    def __init__(self, data):
        grid = defaultdict(int)
        seen_double = set()

        for (x1, y1, x2, y2) in data:
            # print(f"Consider {x1} {y1} -> {x2} {y2}")
            if x1 == x2:
                for y in getrange(y1, y2):
                    # print(f"Mark {x1} {y}")
                    grid[x1, y] += 1
                    if grid[x1, y] > 1:
                        # print("It's double")
                        seen_double.add((x1, y))
            elif y1 == y2:
                for x in getrange(x1, x2):
                    # print(f"Mark {x} {y1}")
                    grid[x, y1] += 1
                    if grid[x, y1] > 1:
                        # print("It's double")
                        seen_double.add((x, y1))
            else:
                # print(f"Diag: {x1} {y1} -> {x2} {y2}")
                for (x, y) in zip(getrange(x1, x2), getrange(y1, y2)):
                    # print(f"{x} {y}")
                    grid[x, y] += 1
                    if grid[x, y] > 1:
                        seen_double.add((x, y))

        self.double_count = len(seen_double)


class Day05:
    """ AoC 2021 Day 05 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 05 part 1 """
        data = parse(filename)
        if len(data) < 20:
            print(data)
        b = Board(data)
        return b.double_count
        return -1

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 05 part 2 """
        data = parse(filename)
        if len(data) < 20:
            print(data)
        return -1
