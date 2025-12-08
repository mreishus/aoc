#!/usr/bin/env python
"""
Advent Of Code 2025 Day 7
https://adventofcode.com/2025/day/7
"""

from functools import cache

class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[(x, y)] = char
                    self.max_x = max(self.max_x, x)
                    x += 1
                self.max_y = max(self.max_y, y)
                y += 1
                x = 0

    def display(self):
        for y in range(self.max_y + 1):
            row = ""
            for x in range(self.max_x + 1):
                row += self.grid[(x, y)]
            print(row)

    @cache
    def beam_count(self, x, y):
        if (x, y) not in self.grid:
            return 0

        char = self.grid[(x, y)]
        if char == 'S':
            return 1

        r = 0
        if (x+1, y) in self.grid and self.grid[(x+1, y)] == '^':
            r += self.beam_count(x+1, y)
        if (x-1, y) in self.grid and self.grid[(x-1, y)] == '^':
            r += self.beam_count(x-1, y)
        if (x, y-1) in self.grid and self.grid[(x, y-1)] != '^':
            r += self.beam_count(x, y-1)
        return r

    def solve1(self):
        count = 0
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                if self.grid[(x, y)] == '^' and self.beam_count(x, y) > 0:
                    count += 1
        return count

    def solve2(self):
        y = self.max_y
        count = 0
        for x in range(0, self.max_x + 1):
            count += self.beam_count(x, y)
        return count

class Day07:
    """AoC 2025 Day 07"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.solve1()

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.solve2()
