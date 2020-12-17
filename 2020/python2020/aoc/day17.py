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
        self.z_min = 0
        self.z_max = 0
        self.y_min = 0
        self.y_max = 0
        self.x_min = 0
        self.x_max = 0
        self.w_min = 0
        self.w_max = 0
        self.is_4d = False
        self.parse(filename)

    def make_it_4d(self):
        self.is_4d = True

    def parse(self, filename):
        grid = defaultdict(int)
        loc = complex(0, 0)
        x = 0
        y = 0
        z = 0
        w = 0

        with open(filename) as f:
            for line in f:
                for char in line.strip():
                    grid[x, y, z, w] = 1 if char == "#" else 0
                    x += 1
                    self.x_max = max(self.x_max, x)
                y += 1
                x = 0
                self.y_max = y
        self.grid = grid

    def step(self):
        self.expand_grid()
        new_grid = copy(self.grid)
        for w in range(self.w_min, self.w_max + 1):
            for z in range(self.z_min, self.z_max + 1):
                for x in range(self.x_min, self.x_max + 1):
                    for y in range(self.y_min, self.y_max + 1):
                        neighbors = sum(
                            self.grid[n] for n in self.gen_neighbors(x, y, z, w)
                        )
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

    def expand_grid(self):
        self.z_min -= 1
        self.z_max += 1
        self.y_min -= 1
        self.y_max += 1
        self.x_min -= 1
        self.x_max += 1
        if self.is_4d:
            self.w_min -= 1
            self.w_max += 1

    def display(self, z):
        w = 0
        for y in range(5):
            for x in range(5):
                char = self.grid[x, y, z, w]
                print(char, end="")
            print("")


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
