#!/usr/bin/env python
"""
Advent Of Code 2023 Day 10
https://adventofcode.com/2023/day/10
"""
import re
from typing import List
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    return line


class Grid:
    def __init__(self):
        self.grid = {}
        self.grid = defaultdict(lambda: ".", self.grid)
        self.distances = {}

        self.max_x = 0
        self.max_y = 0
        self.start = (0, 0)

    def parse(self, filename: str):
        self.max_x = 0
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[x, y] = char

                    if char == "S":
                        self.start = (x, y)
                        starts = {
                            "../inputs/10/input_small.txt": "F",
                            "../inputs/10/input_small2.txt": "F",
                            "../inputs/10/input_small3.txt": "F",
                            "../inputs/10/input_small4.txt": "F",
                            "../inputs/10/input_small5.txt": "F",
                            "../inputs/10/input_small6.txt": "F",
                            "../inputs/10/input_small7.txt": "F",
                            "../inputs/10/input.txt": "|",
                        }
                        if filename in starts:
                            self.grid[x, y] = starts[filename]
                            print("Overriding start position to", starts[filename])

                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def parse2(self, filename: str):
        ## Just like parse, except we parse at double the resolution.
        self.max_x = 0
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    if char == "S":
                        self.start = (x, y)
                        starts = {
                            "../inputs/10/input_small.txt": "F",
                            "../inputs/10/input_small2.txt": "F",
                            "../inputs/10/input_small3.txt": "F",
                            "../inputs/10/input_small4.txt": "F",
                            "../inputs/10/input_small5.txt": "F",
                            "../inputs/10/input_small6.txt": "F",
                            "../inputs/10/input_small7.txt": "F",
                            "../inputs/10/input_small8.txt": "7",
                            "../inputs/10/input.txt": "|",
                        }
                        if filename in starts:
                            char = starts[filename]
                            print("Overriding start position to", starts[filename])

                    if char == "|":
                        self.grid[x, y] = "|"
                        self.grid[x, y + 1] = "|"
                    elif char == "-":
                        self.grid[x, y] = "-"
                        self.grid[x + 1, y] = "-"
                    elif char == "L":
                        self.grid[x, y] = "L"
                        self.grid[x + 1, y] = "-"
                    elif char == "J":
                        self.grid[x, y] = "J"
                    elif char == "7":
                        self.grid[x, y] = "7"
                        self.grid[x, y + 1] = "|"
                    elif char == "F":
                        self.grid[x, y] = "F"
                        self.grid[x + 1, y] = "-"
                        self.grid[x, y + 1] = "|"

                    x += 2
                    self.max_x = max(self.max_x, x)
                y += 2
                x = 0
                self.max_y = max(self.max_y, y)

    def part1(self):
        max_distance, distances = self.flood(self.start)
        return max_distance // 2

    def part2(self):
        max_distance, loop_distances = self.flood(self.start)
        # print("Max distance:", max_distance)
        # print("Loop distances:", loop_distances)

        ## Delete Junk
        for x in range(0, self.max_x, 2):
            for y in range(0, self.max_y, 2):
                all_four = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
                if not any([(xx, yy) in loop_distances for xx, yy in all_four]):
                    for xx, yy in all_four:
                        self.grid[xx, yy] = "."

        outside_max, outside_distances = self.flood((-1, -1))
        # print("Outside max distance:", outside_max)
        # print("Outside distances:", outside_distances)

        print("")
        # self.display2([])
        self.display2(outside_distances)

        surrounded = 0
        for x in range(0, self.max_x, 2):
            for y in range(0, self.max_y, 2):
                all_four = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
                ## Check if all four are . in grid
                if all([self.grid[xx, yy] == "." for xx, yy in all_four]):
                    ## Check if all four are in outside_distances
                    if not all([(xx, yy) in outside_distances for xx, yy in all_four]):
                        surrounded += 1
                        print("Surrounded:", x, y)
        return surrounded

    def display2(self, outside_distances):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) in outside_distances:
                    print("O", end="")
                else:
                    print(self.grid[x, y], end="")
            print()

    def flood(self, begin=None, stop_early=999999999999):
        q = [(begin, 0)]
        distances = {}
        distances[begin] = 0

        max_distance = 0
        i = 0
        while len(q) > 0:
            i += 1
            if i > stop_early:
                return max_distance, distances
            (x, y), distance = q.pop(0)
            max_distance = max(max_distance, distance)
            # print(x, y)
            for xx, yy in self.get_neighbours(x, y):
                if (xx, yy) not in distances:
                    # print("  ", xx, yy, "==", self.grid[xx, yy], "  ", distance + 1)
                    distances[xx, yy] = distance + 1
                    q.append(((xx, yy), distance + 1))
        return max_distance, distances

    def get_neighbours(self, x, y):
        char = self.grid[x, y]
        cands = []
        if char == "|":
            cands = [(x, y - 1), (x, y + 1)]
        elif char == "-":
            cands = [(x - 1, y), (x + 1, y)]
        elif char == "L":
            cands = [(x, y - 1), (x + 1, y)]
        elif char == "J":
            cands = [(x, y - 1), (x - 1, y)]
        elif char == "7":
            cands = [(x, y + 1), (x - 1, y)]
        elif char == "F":
            cands = [(x, y + 1), (x + 1, y)]
        else:
            cands = []
            for a, b in [
                (x, y - 1),
                (x, y + 1),
                (x - 1, y),
                (x + 1, y),
            ]:
                if self.grid[a, b] == ".":
                    cands.append((a, b))
        for xx, yy in cands:
            # if 0 <= xx <= self.max_x and 0 <= yy <= self.max_y:
            if -1 <= xx <= (self.max_x + 1) and -1 <= yy <= (self.max_y + 1):
                yield (xx, yy)

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                print(self.grid[x, y], end="")
            print()


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


class Day10:
    """AoC 2023 Day 10"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse2(filename)
        return g.part1()

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse2(filename)
        return g.part2()
