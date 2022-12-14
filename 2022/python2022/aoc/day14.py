#!/usr/bin/env python
"""
Advent Of Code 2022 Day 14
https://adventofcode.com/2022/day/14
"""
from collections import defaultdict
import time


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    coords = line.split(" -> ")
    return [list(map(int, c.split(","))) for c in coords]


class Grid:
    def __init__(self):
        self.grid = defaultdict(lambda: ".")
        self.spigot = (500, 0)

    def load_data(self, data):
        for line in data:
            oldx, oldy = None, None
            while line:
                [x, y] = line.pop(0)
                if oldx is not None and oldy is not None:
                    self.draw_wall(oldx, oldy, x, y)
                oldx, oldy = x, y
        self.grid[500, 0] = "+"
        self.maxy_after_load = max(y for x, y in self.grid.keys())

    def draw_wall(self, x1, y1, x2, y2):
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.grid[(x1, y)] = "#"
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.grid[(x, y1)] = "#"

    def display(self):
        minx = min(x for x, y in self.grid.keys())
        maxx = max(x for x, y in self.grid.keys())
        miny = min(y for x, y in self.grid.keys())
        maxy = max(y for x, y in self.grid.keys())
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                print(self.grid[x, y], end="")
            print("")
        print(minx, maxx, miny, maxy)

    def possible_sand_moves(self, x, y):
        yield (x, y + 1)  # Down
        yield (x - 1, y + 1)  # Down left
        yield (x + 1, y + 1)  # Down right

    def get_grid(self, x, y, p2):
        if not p2:
            return self.grid[x, y]
        if y >= self.maxy_after_load + 2:
            return "#"
        return self.grid[x, y]

    def new_sand(self, p2):
        (x, y) = self.spigot

        while True:
            moved = False
            if self.grid[500, 0] == "O":
                return False

            for (x1, y1) in self.possible_sand_moves(x, y):
                if y1 > self.maxy_after_load + 5:
                    return False

                char = self.get_grid(x1, y1, p2)
                if char == "#" or char == "O":
                    continue
                x, y = x1, y1
                moved = True
                break
            if not moved:
                self.grid[x, y] = "O"
                break
        return True


class Day14:
    """AoC 2022 Day 14"""

    @staticmethod
    def part1(filename: str) -> int:
        print("")
        data = parse(filename)
        g = Grid()
        g.load_data(data)
        g.display()

        count = 0
        while True:
            added_new_sand = g.new_sand(False)
            if not added_new_sand:
                break
            count += 1
            # g.display()
        print("Added", count, "new sand")
        return count

    @staticmethod
    def part2(filename: str) -> int:
        print("")
        data = parse(filename)
        g = Grid()
        g.load_data(data)
        g.display()

        count = 0
        while True:
            added_new_sand = g.new_sand(True)
            if not added_new_sand:
                break
            count += 1
        print("Added", count, "new sand")
        return count
