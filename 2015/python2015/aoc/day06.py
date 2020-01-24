#!/usr/bin/env python
"""
Advent Of Code 2015 Day 6
https://adventofcode.com/2015/day/6
"""

import re
import numpy as np
from typing import Tuple
from aoc.parsers import all_lines

parser = re.compile(r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)")


def parse_line(line: str) -> Tuple[str, int, int, int, int]:
    (instruction, x1, y1, x2, y2) = re.search(parser, line).groups()
    return (instruction, int(x1), int(y1), int(x2), int(y2))


def part1(commands):
    grid = np.zeros((1000, 1000), dtype=np.bool)
    for (instruction, x1, y1, x2, y2) in commands:
        if instruction == "turn on":
            grid[y1 : y2 + 1, x1 : x2 + 1] = 1
        elif instruction == "turn off":
            grid[y1 : y2 + 1, x1 : x2 + 1] = 0
        elif instruction == "toggle":
            grid[y1 : y2 + 1, x1 : x2 + 1] = np.logical_not(
                grid[y1 : y2 + 1, x1 : x2 + 1]
            )
        else:
            raise ValueError("Unknown instrction")
    return np.count_nonzero(grid)


def part2(commands):
    grid = np.zeros((1000, 1000), dtype=int)
    for (instruction, x1, y1, x2, y2) in commands:
        if instruction == "turn on":
            grid[y1 : y2 + 1, x1 : x2 + 1] += 1
        elif instruction == "turn off":
            grid[y1 : y2 + 1, x1 : x2 + 1] -= 1
            grid[y1 : y2 + 1, x1 : x2 + 1] = np.maximum(
                0, grid[y1 : y2 + 1, x1 : x2 + 1]
            )
        elif instruction == "toggle":
            grid[y1 : y2 + 1, x1 : x2 + 1] += 2
        else:
            raise ValueError("Unknown instrction")
    return np.sum(grid)


class Day06:
    """ AoC 2015 Day 06 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 06 part 1 """
        commands = [parse_line(line) for line in all_lines(filename)]
        return part1(commands)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 06 part 2 """
        commands = [parse_line(line) for line in all_lines(filename)]
        return part2(commands)
