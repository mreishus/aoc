#!/usr/bin/env python
"""
Advent Of Code 2015 Day 18
https://adventofcode.com/2015/day/18
"""

import copy
import numpy as np
from aoc.parsers import all_lines


def parse_line(line: str):
    return [1 if char == "#" else 0 for char in line]


def step2(grid):
    # Corner lights are stuck on
    grid[0, 0] = 1
    grid[0, -1] = 1
    grid[-1, 0] = 1
    grid[-1, -1] = 1
    grid = step(grid)
    grid[0, 0] = 1
    grid[0, -1] = 1
    grid[-1, 0] = 1
    grid[-1, -1] = 1
    return grid


def step(grid):
    neighbors = np.zeros(grid.shape, dtype=int)

    # Cardinal
    neighbors[1:] += grid[:-1]
    neighbors[:-1] += grid[1:]
    neighbors[:, 1:] += grid[:, :-1]
    neighbors[:, :-1] += grid[:, 1:]

    # Diagonal
    neighbors[1:, 1:] += grid[:-1, :-1]
    neighbors[1:, :-1] += grid[:-1, 1:]
    neighbors[:-1, 1:] += grid[1:, :-1]
    neighbors[:-1, :-1] += grid[1:, 1:]

    # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
    # So: 3 neighbors = Always on
    #     2 neighbors = had to have been on before
    n3 = neighbors == 3
    n2 = neighbors == 2
    grid = grid & n2
    grid = grid | n3
    return grid


def part1(grid, steps):
    grid = copy.deepcopy(grid)
    for _ in range(steps):
        grid = step(grid)
    return (grid == 1).sum()


def part2(grid, steps):
    grid = copy.deepcopy(grid)
    for _ in range(steps):
        grid = step2(grid)
    return (grid == 1).sum()


class Day18:
    """ AoC 2015 Day 18 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 18 part 1 """
        grid = np.array([parse_line(x) for x in all_lines(filename)])
        return part1(grid, 100)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 18 part 2 """
        grid = np.array([parse_line(x) for x in all_lines(filename)])
        return part2(grid, 100)
