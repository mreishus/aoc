#!/usr/bin/env python
"""
Advent Of Code 2022 Day 12
https://adventofcode.com/2022/day/12
"""
from collections import deque
from functools import cache
from typing import NamedTuple

State = NamedTuple("State", [("loc", tuple[int, int]), ("steps", int)])


class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.start = None
        self.end = None
        self.aas = []

    def parse(self, filename: str):
        self.max_x = 0
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[x, y] = self.fix_elevation(char)
                    if char == "S":
                        self.start = x, y
                        self.aas.append((x, y))
                    elif char == "E":
                        self.end = x, y
                    elif char == "a":
                        self.aas.append((x, y))
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def fix_elevation(self, letter):
        if letter == "S":
            return "a"
        elif letter == "E":
            return "z"
        return letter

    @cache
    def get_raw_neighbors(self, x, y):
        x_size = self.max_x
        y_size = self.max_y
        cands = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        for (xx, yy) in cands:
            if xx >= 0 and xx < x_size and yy >= 0 and yy < y_size:
                yield xx, yy

    @cache
    def get_neighbors(self, loc):
        x, y = loc
        height = ord(self.grid[x, y])
        for (xx, yy) in self.get_raw_neighbors(x, y):
            this_height = ord(self.grid[xx, yy])
            if this_height <= (height + 1):
                yield xx, yy

    def part2(self):
        cand = []
        for aa in self.aas:
            self.start = aa

            ### These lines kill the performance, but
            ### they are needed to get the correct answer
            self.get_neighbors.cache_clear()
            self.get_raw_neighbors.cache_clear()
            ### There's a 10x speedup if I learn how they can be removed

            ## Possible performance gain:
            ## Tell BFS the min number of steps we've already found,
            ## it can cancel its search if it goes over that number.
            z = self.bfs()
            if z is not None:
                cand.append(z)
        return min(cand)

    def bfs(self) -> (int | None):
        if self.start is None or self.end is None:
            return None

        init = State(self.start, 0)
        queue = deque([init])
        visited = set()
        while queue:
            state = queue.popleft()

            if state.loc in visited:
                continue
            visited.add(state.loc)

            if state.loc == self.end:
                return state.steps

            for loc in self.get_neighbors(state.loc):
                if loc not in visited:
                    queue.append(State(loc, state.steps + 1))

        return None


class Day12:
    """AoC 2022 Day 12"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.bfs()

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.part2()
