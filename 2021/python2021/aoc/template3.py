#!/usr/bin/env python
"""
Advent Of Code 2021 Day 08
https://adventofcode.com/2021/day/8
"""
from typing import List
import re
from collections import defaultdict

PARSER = re.compile(r"thing (\d+),(\d+), stuff")


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]
        # lines = file.read().strip()
        # first, *blocks = lines.split("\n\n")
        # return (first, blocks)


def parse_line(line):
    return line
    # (d, amount) = line.split(" ")
    # return (d, int(amount))


def parse_line2(line):
    (x, y) = re.search(PARSER, line).groups()
    return (x, y)


def first_line(filename: str) -> str:
    """ Given a filename, returns the first line of a file. """
    with open(filename) as file:
        return file.readline().strip()


def all_lines(filename: str) -> List[str]:
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


class Day08:
    """ AoC 2021 Day 08 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 08 part 1 """
        data = parse(filename)
        if len(data) < 20:
            print(data)
        return -1

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 08 part 2 """
        data = parse(filename)
        if len(data) < 20:
            print(data)
        return -1
