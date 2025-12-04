#!/usr/bin/env python
"""
Advent Of Code 2025 Day 4
https://adventofcode.com/2025/day/4
"""

class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.removable = []

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


    def mark_removable(self):
        self.removable = []
        for y in range(0, self.max_y+1):
            for x in range(0, self.max_x+1):
                roll_count = 0
                if self.grid[(x, y)] == '@':
                    for xx, yy in self.get_neighbors(x, y):
                        if self.grid[(xx, yy)] == '@':
                            roll_count += 1
                        if roll_count >= 4:
                            break
                    if roll_count < 4:
                        self.removable.append( (x, y) )

    def solve1(self):
        self.removable = []
        self.mark_removable()
        return len(self.removable)

    def solve2(self):
        removed = 0
        while True:
            self.removable = []
            self.mark_removable()
            if len(self.removable) == 0:
                break
            for x, y in self.removable:
                removed += 1
                self.grid[(x, y)] = '.'
        return removed


    def get_neighbors(self, x, y):
        for dx, dy in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]:
            if (x + dx, y + dy) in self.grid:
                yield (x + dx, y + dy)


class Day04:
    """AoC 2025 Day 04"""

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

