#!/usr/bin/env python
"""
Advent Of Code 2023 Day 21
https://adventofcode.com/2023/day/21
"""
import re
from typing import List
from collections import defaultdict


class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.start = None

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    if char == "S":
                        self.start = (x, y)
                        char = "."
                    self.grid[(x, y)] = char
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                print(self.grid[(x, y)], end="")
            print()

    def display_with_visited(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) in self.finish_locations:
                    print("O", end="")
                else:
                    print(self.grid[(x, y)], end="")
            print()

    def bfs(self, start, max_dist=6):
        visited = set()
        finish_locations = set()
        queue = [(start, 0)]
        while queue:
            loc, dist = queue.pop(0)
            if (loc, dist) not in visited:
                visited.add((loc, dist))
                if dist == max_dist:
                    finish_locations.add(loc)
                # queue.extend(self.get_neighbors(node))
                if dist < max_dist:
                    for n in self.get_neighbors(loc):
                        queue.append((n, dist + 1))
        self.visited = visited
        self.finish_locations = finish_locations
        return finish_locations

    def get_neighbors(self, node):
        neighbors = []
        x, y = node
        possibilities = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        for xx, yy in possibilities:
            if (xx, yy) in self.grid and self.grid[(xx, yy)] != "#":
                neighbors.append((xx, yy))
        return neighbors


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


class Day21:
    """AoC 2023 Day 21"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        g.display()
        x = g.bfs(g.start, 64)
        return len(x)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        print(data)
        return 0
