#!/usr/bin/env python
"""
Advent Of Code 2024 Day 18
https://adventofcode.com/2024/day/18
"""
from typing import List
import re
from collections import deque


class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.start = (0, 0)
        self.end = (-1, -1)
        self.dir = (1, 0)
        self.bytes_list = []

    def parse(self, filename):
        bytes_list = []
        with open(filename) as file:
            for line in file:
                [x, y] = ints(line)
                bytes_list.append([x, y])

        self.bytes_list = bytes_list
        if "small" in filename:
            self.end = (6, 6)
            self.max_x = 7
            self.max_y = 7
        else:
            self.end = (70, 70)
            self.max_x = 71
            self.max_y = 71

    def load_bytes(self, myrange):
        for i in myrange:
            [x, y] = self.bytes_list[i]
            self.grid[(x, y)] = "#"

    def display(self, extra=[]):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) in self.grid:
                    print(self.grid[(x, y)], end="")
                else:
                    print(".", end="")
            print()
            self.max_y = max(self.max_y, y)

    def bfs(self, start_loc):
        queue = deque([(start_loc, 0)])
        visited = set()
        while queue:
            loc, steps = queue.popleft()
            (x, y) = loc

            if loc == self.end:
                return steps
            if loc in visited:
                continue
            visited.add(loc)

            for xx, yy in self.get_neighbors(x, y):
                queue.append(((xx, yy), steps + 1))
        return -1

    def get_neighbors(self, x, y):
        for dx, dy in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]:
            xx = x + dx
            yy = y + dy
            if 0 <= xx and xx < self.max_x:
                if 0 <= yy and yy < self.max_y:
                    if (xx, yy) not in self.grid or self.grid[(xx, yy)] != "#":
                        # if (xx == 0):
                        #     not_in_grid = (xx, yy) in self.grid
                        #     print("y", xx, yy, not_in_grid)
                        #     print(self.grid)
                        yield (xx, yy)


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


class Day18:
    """AoC 2024 Day 18"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename, 1024)
        print("")
        g.display()
        return g.bfs((0, 0))
        return g.solve()

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        for i in range(len(g.bytes_list)):
            g.load_bytes(range(i))
            answer = g.bfs((0, 0))
            if answer == -1:
                return g.bytes_list[i - 1]
        return None
