#!/usr/bin/env python
"""
Advent Of Code 2022 Day 04
https://adventofcode.com/2022/day/3
"""


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    pairs = line.split(",")
    return [list(map(int, pair.split("-"))) for pair in pairs]


class Day04:
    """AoC 2022 Day 04"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        count = 0
        for assignment_pair in data:
            [[a, b], [c, d]] = assignment_pair
            if a <= c and b >= d:
                count += 1
            elif c <= a and d >= b:
                count += 1
        return count

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        count = 0
        for assignment_pair in data:
            [[a, b], [c, d]] = assignment_pair
            if a <= c <= b:
                count += 1
            elif c <= a <= d:
                count += 1
        return count
