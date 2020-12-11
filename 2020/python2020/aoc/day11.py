#!/usr/bin/env python
"""
Advent Of Code 2020 Day 11
https://adventofcode.com/2020/day/11


1000 = 8 = . Floor
0000 = 0 = L Empty
0001 = 1 = # Occupied

"""

import functools
import numpy as np


def parse(filename: str):
    with open(filename) as file:
        return np.array([parse_line(line.strip()) for line in file.readlines()])


def parse_line(line: str):
    return [0 if char == "L" else 8 for char in line]


def step(grid):
    neighbors = np.zeros(grid.shape, dtype=int)

    # Cardinal
    neighbors[1:] += grid[:-1] & 1
    neighbors[:-1] += grid[1:] & 1
    neighbors[:, 1:] += grid[:, :-1] & 1
    neighbors[:, :-1] += grid[:, 1:] & 1

    # Diagonal
    neighbors[1:, 1:] += grid[:-1, :-1] & 1
    neighbors[1:, :-1] += grid[:-1, 1:] & 1
    neighbors[:-1, 1:] += grid[1:, :-1] & 1
    neighbors[:-1, :-1] += grid[1:, 1:] & 1

    # If a seat is empty (L) and there are no occupied seats adjacent to it,
    # the seat becomes occupied.
    empty = grid == 0
    set_to_occupied = empty & (neighbors == 0)

    # If a seat is occupied (#) and four or more seats adjacent to it are also
    # occupied, the seat becomes empty.
    occupied = grid & 1
    set_to_empty = occupied & (neighbors >= 4)

    return (grid | set_to_occupied) & ~set_to_empty


def step2_raycast(grid):
    rays = {}

    rows = grid.shape[0]  # If rows = 10, then y = 0-9 are valid
    cols = grid.shape[1]  # If cols = 10, then x = 0-9 are valid

    directions = [ (x, y) for x in range(-1, 2) for y in range (-1, 2) if not ( (x == 0) and (y == 0)) ]

    def valid(pair):
        x, y = pair
        return 0 <= y < rows and 0 <= x < cols

    for y in range(0, rows):
        for x in range(0, cols):

            neighbors = []

            dx, dy = x, y
            for d in directions:
                dx = x + d[0]
                dy = y + d[1]
                while valid((dx, dy)):
                    if grid[dy, dx] != 8:
                        neighbors.append((dx, dy))
                        break
                    dx += d[0]
                    dy += d[1]

            rays[ (x, y) ] = neighbors

    return rays

def step2(grid):
    neighbors = np.zeros(grid.shape, dtype=int)

    rows = grid.shape[0]  # If rows = 10, then y = 0-9 are valid
    cols = grid.shape[1]  # If cols = 10, then x = 0-9 are valid

    rays = step2_raycast(grid)

    for y in range(0, rows):
        for x in range(0, cols):
            ncount = 0

            for (x1, y1) in rays[ (x, y) ]:
                if grid[y1, x1] == 1:
                    ncount += 1

            neighbors[y, x] = ncount

    # If a seat is empty (L) and there are no occupied seats adjacent to it,
    # the seat becomes occupied.
    empty = grid == 0
    set_to_occupied = empty & (neighbors == 0)

    # If a seat is occupied (#) and five or more seats adjacent to it are also
    # occupied, the seat becomes empty.
    occupied = grid & 1
    set_to_empty = occupied & (neighbors >= 5)

    return (grid | set_to_occupied) & ~set_to_empty


def part1(grid):
    while True:
        last_grid = grid
        grid = step(grid)
        if np.array_equal(last_grid, grid):
            break
    return np.count_nonzero(grid == 1)


def part2(grid):
    while True:
        last_grid = grid
        grid = step2(grid)
        if np.array_equal(last_grid, grid):
            break
    return np.count_nonzero(grid == 1)


class Day11:
    """ AoC 2020 Day 11 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 09 part 1 """
        grid = parse(filename)
        return part1(grid)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 09 part 2 """
        grid = parse(filename)
        return part2(grid)
