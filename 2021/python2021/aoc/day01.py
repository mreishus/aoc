#!/usr/bin/env python
"""
Advent Of Code 2021 Day 1
https://adventofcode.com/2021/day/1
"""
from typing import List


def parse(filename: str) -> List[int]:
    with open(filename) as file:
        return [int(line.strip()) for line in file.readlines()]


def increase_count(data: List[int], window: int) -> int:
    return sum(b > a for (a, b) in zip(data, data[window:]))


class Day01:
    """AoC 2021 Day 01"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return increase_count(data, 1)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return increase_count(data, 3)
