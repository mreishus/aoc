#!/usr/bin/env python
"""
Advent Of Code 2023 Day 9
https://adventofcode.com/2023/day/9
"""
import re
from typing import List


def parse(filename: str):
    with open(filename) as file:
        return [ints(line.strip()) for line in file.readlines()]


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def get_diffs(line):
    return [line[i + 1] - line[i] for i in range(len(line) - 1)]


def get_diffs2(line):
    return [line[i] - line[i + 1] for i in range(len(line) - 1)]


class Day09:
    """AoC 2023 Day 09"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        total = 0
        for line in data:
            x = []
            differences = get_diffs(line)
            while not all(d == 0 for d in differences):
                x.append(differences)
                differences = get_diffs(differences)

            next_num = line[-1] + sum([item[-1] for item in x])
            total += next_num
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        total = 0
        for line in data:
            x = []
            differences = get_diffs2(line)
            while not all(d == 0 for d in differences):
                x.append(differences)
                differences = get_diffs2(differences)

            next_num = line[0] + sum([item[0] for item in x])
            total += next_num
        return total
