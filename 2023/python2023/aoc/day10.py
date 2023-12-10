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

    def flood(self):
        print("flood")

        q = [(self.start, 0)]
        self.distances[self.start] = 0

        max_distance = 0
        while len(q) > 0:
            (x, y), distance = q.pop(0)
            max_distance = max(max_distance, distance)
            # print(x, y)
            for xx, yy in self.get_neighbours(x, y):
                if (xx, yy) not in self.distances:
                    # print("  ", xx, yy, "==", self.grid[xx, yy], "  ", distance + 1)
                    self.distances[xx, yy] = distance + 1
                    q.append(((xx, yy), distance + 1))
        return max_distance

    def get_neighbours(self, x, y):
        char = self.grid[x, y]
        if char == "|":
            return [(x, y - 1), (x, y + 1)]
        elif char == "-":
            return [(x - 1, y), (x + 1, y)]
        elif char == "L":
            return [(x, y - 1), (x + 1, y)]
        elif char == "J":
            return [(x, y - 1), (x - 1, y)]
        elif char == "7":
            return [(x, y + 1), (x - 1, y)]
        elif char == "F":
            return [(x, y + 1), (x + 1, y)]
        return []


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


class Day10:
    """AoC 2023 Day 10"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.flood()

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        print(data)
        return 1
