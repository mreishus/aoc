#!/usr/bin/env python
"""
Advent Of Code 2021 Day 04
https://adventofcode.com/2021/day/4
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


class Day04:
    """ AoC 2021 Day 04 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 04 part 1 """
        data = parse(filename)
        if len(data) < 20:
            print(data)
        return 4

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 04 part 2 """
        data = parse(filename)
        if len(data) < 20:
            print(data)
        return 4 * 4
