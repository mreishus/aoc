#!/usr/bin/env python
"""
Advent Of Code 2023 Day 11
https://adventofcode.com/2023/day/11
"""


class Grid:
    def __init__(self):
        self.grid = {}

        self.max_x = 0
        self.max_y = 0
        self.galaxies = []

        self.expanding_x = set()
        self.expanding_y = set()

    def parse(self, filename: str):
        x = 0
        y = 0

        xs_with_galaxies = set()
        ys_with_galaxies = set()

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[(x, y)] = char
                    if char == "#":
                        xs_with_galaxies.add(x)
                        ys_with_galaxies.add(y)
                        self.galaxies.append((x, y))
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

        all_x = set(range(self.max_x))
        all_y = set(range(self.max_y))

        self.expanding_x = all_x - xs_with_galaxies
        self.expanding_y = all_y - ys_with_galaxies

    def find_pathlen_between_galaxies(self, g_start, g_end, expand_by=1):
        x_start, y_start = self.galaxies[g_start]
        x_end, y_end = self.galaxies[g_end]

        x_diff = self.calculate_range(x_start, x_end, self.expanding_x, expand_by)
        y_diff = self.calculate_range(y_start, y_end, self.expanding_y, expand_by)
        return x_diff + y_diff

    def calculate_range(self, start, end, expanding, expand_by):
        step = -1 if start > end else 1

        range_set = set(range(start, end, step))
        expanding_count = len(range_set.intersection(expanding))
        distance = len(range_set) + expanding_count * expand_by
        return distance

    def part1(self, expand_by=1):
        total = 0
        i = 0
        for g_start in range(len(self.galaxies)):
            for g_end in reversed(range(g_start + 1, len(self.galaxies))):
                pathlen = self.find_pathlen_between_galaxies(g_start, g_end, expand_by)
                total += pathlen
            i += 1
        return total

    def part2(self):
        return self.part1(1000000 - 1)


class Day11:
    """AoC 2023 Day 11"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.part1()

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.part2()
