#!/usr/bin/env python
"""
Advent Of Code 2021 Day 1
https://adventofcode.com/2021/day/1
"""
from typing import List, Optional


def parse(filename: str) -> List[int]:
    with open(filename) as file:
        return [int(line.strip()) for line in file.readlines()]


class Day01:
    """ AoC 2021 Day 01 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 01 part 1 """
        data = parse(filename)
        return sum(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 01 part 2 """
        data = parse(filename)
        return sum(data) + 1
