#!/usr/bin/env python
"""
Advent Of Code 2020 Day 24
https://adventofcode.com/2020/day/24
"""

import re
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Coord:
    x: int = 0
    y: int = 0
    z: int = 0

    # Move in hex grid, using cube coordinates
    # See https://www.redblobgames.com/grids/hexagons/#neighbors-cube
    def move(self, dr):
        if dr == "nw":
            self.x += 0
            self.y += 1
            self.z += -1
        elif dr == "ne":
            self.x += 1
            self.y += 0
            self.z += -1
        elif dr == "w":
            self.x += -1
            self.y += 1
            self.z += 0
        elif dr == "e":
            self.x += 1
            self.y += -1
            self.z += 0
        elif dr == "se":
            self.x += 0
            self.y += -1
            self.z += 1
        elif dr == "sw":
            self.x += -1
            self.y += 0
            self.z += 1

    def __hash__(self):
        return hash((self.x, self.y, self.z))


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    result = []

    while len(line) > 0:
        a = re.match(r"(e|se|sw|w|nw|ne)", line)
        if not a:
            return result
        found = a.groups()[0]
        result.append(found)
        line = line[len(found) :]
    return result


def p1_calc_grid(data):
    grid = defaultdict(int)
    for line in data:
        coord = Coord()
        for direc in line:
            coord.move(direc)
        if grid[coord] == 1:
            grid[coord] = 0
        else:
            grid[coord] = 1
    return grid


def p1(data):
    grid = p1_calc_grid(data)
    return sum(g for g in grid.values() if g == 1)


def p2(data):
    grid = p1_calc_grid(data)
    for i in range(100):
        grid = step(grid)
        # s = sum(g for g in grid.values() if g == 1)
        # print(f"Step {i+1}: {s}")
    return sum(g for g in grid.values() if g == 1)


def get_neighbors(c: Coord):
    (x, y, z) = c.x, c.y, c.z
    yield Coord(x + 0, y + 1, z - 1)  # nw
    yield Coord(x + 1, y + 0, z - 1)  # ne
    yield Coord(x - 1, y + 1, z + 0)  # w
    yield Coord(x + 1, y - 1, z + 0)  # e
    yield Coord(x + 0, y - 1, z + 1)  # se
    yield Coord(x - 1, y + 0, z + 1)  # sw


def step(grid):
    max_x, max_y = 0, 0
    min_x, min_y = 0, 0

    new_grid = defaultdict(int)

    for c in grid.keys():
        max_x = max(max_x, c.x)
        max_y = max(max_y, c.y)
        min_x = min(min_x, c.x)
        min_y = min(min_y, c.y)

    # TODO Optimization: Should check only "1" tiles and neighbors of "1" tiles
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            z = -1 * (x + y)
            c = Coord(x, y, z)

            # Count Neighbors
            n_count = 0
            for n in get_neighbors(c):
                if grid[n] == 1:
                    n_count += 1

            if grid[c] == 1:
                # Any black tile with zero or more than 2 black tiles immediately adjacent
                # to it is flipped to white.
                if n_count == 0 or n_count > 2:
                    new_grid[c] = 0
                else:
                    new_grid[c] = 1
            elif grid[c] == 0:
                # Any white tile with exactly 2 black tiles immediately adjacent to it is
                # flipped to black.
                if n_count == 2:
                    new_grid[c] = 1
                else:
                    new_grid[c] = 0

    return new_grid


class Day24:
    """ AoC 2020 Day 24 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 24 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 24 part 2 """
        data = parse(filename)
        return p2(data)
