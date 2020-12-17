#!/usr/bin/env python
"""
Advent Of Code 2020 Day 17
https://adventofcode.com/2020/day/17
"""

from collections import defaultdict
from copy import copy


class Grid:
    def __init__(self, filename):
        self.grid = None
        self.is_4d = False
        self.parse(filename)

    def make_it_4d(self):
        self.is_4d = True

    def parse(self, filename):
        grid = defaultdict(int)
        x = 0
        y = 0
        z = 0
        w = 0

        with open(filename) as f:
            for line in f:
                for char in line.strip():
                    grid[x, y, z, w] = 1 if char == "#" else 0
                    x += 1
                y += 1
                x = 0
        self.grid = grid

    def step(self):
        new_grid = copy(self.grid)

        # Only consider active squares and those adjacent to active squares
        to_consider = set()
        for k, v in self.grid.items():
            if v == 0:
                continue
            (x, y, z, w) = k
            to_consider.add(k)
            for n in self.gen_neighbors(x, y, z, w):
                to_consider.add(n)

        for (x, y, z, w) in to_consider:
            neighbors = self.neighbor_count(x, y, z, w)
            if self.grid[x, y, z, w] == 1:
                new_val = 0
                if neighbors in (2, 3):
                    new_val = 1
            else:
                new_val = 0
                if neighbors == 3:
                    new_val = 1
            new_grid[x, y, z, w] = new_val

        self.grid = new_grid

    def neighbor_count(self, x, y, z, w):
        count = 0
        for n in self.gen_neighbors(x, y, z, w):
            if self.grid[n] == 1:
                count += 1
                # Optimization: Don't care about counts beyond 4
                if count >= 4:
                    return count
        return count

    def gen_neighbors(self, x, y, z, w):
        w_range = [0]
        if self.is_4d:
            w_range = range(w - 1, w + 2)

        for aw in w_range:
            for ax in range(x - 1, x + 2):
                for ay in range(y - 1, y + 2):
                    for az in range(z - 1, z + 2):
                        if ax == x and ay == y and az == z and aw == w:
                            continue
                        yield ax, ay, az, aw


class Day17:
    """ AoC 2020 Day 17 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 17 part 1 """
        g = Grid(filename)
        for _ in range(6):
            g.step()
        return sum(g.grid.values())

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 17 part 2 """
        g = Grid(filename)
        g.make_it_4d()
        for _ in range(6):
            g.step()
        return sum(g.grid.values())
