#!/usr/bin/env python
"""
Advent Of Code 2022 Day 06
https://adventofcode.com/2022/day/6
"""


def parse(filename: str):
    with open(filename) as file:
        return file.read().strip()


class Day06:
    """AoC 2022 Day 06"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        for i in range(len(data)):
            h = max(i - 4, 0)
            if len(set(data[h:i])) == 4:
                return i
        return -1

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)

        for i in range(len(data)):
            h = max(i - 14, 0)
            if len(set(data[h:i])) == 14:
                return i
        return -1
