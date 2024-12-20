#!/usr/bin/env python
"""
Advent Of Code 2022 Day 02
https://adventofcode.com/2022/day/2
"""
from typing import List
import re

PARSER = re.compile(r"thing (\d+),(\d+), stuff")


def parse(filename: str) -> List[int]:
    with open(filename) as file:
        return [int(line.strip()) for line in file.readlines()]


def parse2(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    return line.split(")")


def parse_line2(line):
    (x, y) = re.search(PARSER, line).groups()
    return (x, y)


def ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"(?:(?<!\d)-)?\d+", s))


class Day02:
    """AoC 2022 Day 02"""

    @staticmethod
    def part1(filename: str) -> int:
        """Given a filename, solve 2022 day 02 part 1"""
        data = parse(filename)
        print(data)
        return 1

    @staticmethod
    def part2(filename: str) -> int:
        """Given a filename, solve 2022 day 02 part 2"""
        data = parse(filename)
        return 1
