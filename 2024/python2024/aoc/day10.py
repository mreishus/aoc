#!/usr/bin/env python
"""
Advent Of Code 2024 Day 10
https://adventofcode.com/2024/day/10
"""
import re
from typing import List
from collections import deque

class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.zeros = []

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    if char.isdigit():
                        char = int(char)
                    self.grid[(x, y)] = char
                    if char == 0:
                        self.zeros.append((x, y))
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def get_trailhead_count(self, start_loc):
        queue = deque(
            [
                start_loc
            ]
        )
        visited = set()
        trailheads = 0
        while queue:
            loc = queue.pop()
            (x, y) = loc
            h = self.grid[loc]

            if loc in visited:
                continue
            visited.add(loc)

            if h == 9:
                # print(f"!!! Trailhead at {x} {y}")
                trailheads += 1

            for xx, yy in self.get_neighbors(x, y):
                hh = self.grid[(xx, yy)]
                if hh == h + 1:
                    # print(f"Append {x} {y} @ {h} --> {xx} {yy} @ {hh}")
                    queue.append( (xx, yy) )
        return trailheads



    def get_neighbors(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if dx != 0 and dy != 0:
                    continue
                if (x + dx, y + dy) in self.grid:
                    yield (x + dx, y + dy)

    def part1(self):
        total = 0

        # print("")
        # print(self.get_trailhead_count(self.zeros[4]))
        # exit()
        for i, loc in enumerate(self.zeros):
            trailhead_count = self.get_trailhead_count(loc)
            # print(f" {i} {loc} = {trailhead_count}")
            total += trailhead_count

        return total

class Day10:
    """AoC 2024 Day 10"""

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
