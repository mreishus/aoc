#!/usr/bin/env python
"""
Advent Of Code 2022 Day 15
https://adventofcode.com/2022/day/15
"""
import re
from collections import defaultdict
from operator import itemgetter


def ints(s: str):
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def parse(filename: str):
    with open(filename) as file:
        return [ints(line.strip()) for line in file.readlines()]


class Grid:
    def __init__(self):
        self.grid = defaultdict(lambda: ".")
        self.sensors = {}
        self.col_exclusions = {}

    def load_data(self, data: list[list[int]]):
        for row in data:
            [sx, sy, bx, by] = row
            self.grid[(sx, sy)] = "S"
            self.grid[(bx, by)] = "B"
            self.sensors[(sx, sy)] = (bx, by)

    def eliminate(self, y_to_compute):
        for (sx, sy), (bx, by) in self.sensors.items():
            print(f"Eliminating sensor {sx} {sy} |  {bx} {by}")
            distance = abs(sx - bx) + abs(sy - by)
            for x in range(sx - distance, sx + distance + 1):
                distance_remaining = distance - abs(sx - x)
                for y in [y_to_compute]:
                    # for y in range(sy - distance_remaining, sy + distance_remaining + 1):
                    if abs(x - sx) + abs(y - sy) <= distance:
                        if self.grid[x, y] == ".":
                            self.grid[x, y] = "#"

    def eliminate2(self, max_x, max_y):
        for (sx, sy), (bx, by) in self.sensors.items():
            print(f"Eliminating2 sensor {sx} {sy} |  {bx} {by}")
            distance = abs(sx - bx) + abs(sy - by)

            ## Range 1: [0, max_x]
            ## Range 2: [sx - distance, sx + distance]
            ## Overlap:
            xrange = range(max(0, sx - distance), min(max_x, sx + distance) + 1)

            xlower = max(0, sx - distance)
            xupper = min(max_x, sx + distance)

            # for x in range(0, max_x + 1):
            for x in xrange:
                # print(x)
                distance_remaining = distance - abs(sx - x)
                ylower = max(0, sy - distance_remaining)
                yupper = min(max_y, sy + distance_remaining) + 1

                thing = (ylower, yupper - 1)
                if x not in self.col_exclusions:
                    self.col_exclusions[x] = []
                self.col_exclusions[x].append(thing)

                # ## Range 1: [0, max_y]
                # ## Range 2: [sy - distance_remaining, sy + distance_remaining]
                # yrange = range(
                #     max(0, sy - distance_remaining),
                #     min(max_y, sy + distance_remaining) + 1,
                # )
                # # for y in range(0, max_y + 1):
                # for y in yrange:
                #     # for y in range(sy - distance_remaining, sy + distance_remaining + 1):
                #     if abs(x - sx) + abs(y - sy) <= distance:
                #         if self.grid[x, y] == ".":
                #             self.grid[x, y] = "#"

    def search(self, max_x, max_y):
        for x in range(0, max_x + 1):
            exes = sorted(self.col_exclusions[x], key=itemgetter(0))

            clear_to = 0
            for (low, high) in exes:
                if low > clear_to:
                    print("Found it! ", x, clear_to)
                    return x * 4000000 + clear_to
                clear_to = max(clear_to, high + 1)

            # for y in range(0, max_y + 1):
            #     if self.grid[x, y] == ".":
            #         self.grid[x, y] = "#"

    def search_old(self, max_x, max_y):
        for x in range(0, max_x + 1):
            for y in range(0, max_y + 1):
                if self.grid[x, y] == ".":
                    print("Found it! ", x, y)
                    return x * 4000000 + y

    def display(self):
        minx = min(x for x, y in self.grid.keys())
        maxx = max(x for x, y in self.grid.keys())
        miny = min(y for x, y in self.grid.keys())
        maxy = max(y for x, y in self.grid.keys())
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                print(self.grid[x, y], end="")
            print("")
            print(y, end="")
        print(minx, maxx, miny, maxy)

    def row_count_hash(self, y):
        minx = min(x for x, y in self.grid.keys())
        maxx = max(x for x, y in self.grid.keys())
        return sum(1 for x in range(minx, maxx + 1) if self.grid[x, y] == "#")


class Day15:
    """AoC 2022 Day 15"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        y_to_compute = 2000000
        if "input_small.txt" in filename:
            y_to_compute = 10

        # print(y_to_compute)
        g = Grid()
        g.load_data(data)
        g.eliminate(y_to_compute)
        return g.row_count_hash(y_to_compute)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)

        min_x = 0
        min_y = 0
        max_x = 4000000
        max_y = 4000000
        if "input_small.txt" in filename:
            max_x = 20
            max_y = 20

        g = Grid()
        g.load_data(data)
        g.eliminate2(max_x, max_y)
        # g.display()
        val = g.search(max_x, max_y)
        return val
