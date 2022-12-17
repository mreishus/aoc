#!/usr/bin/env python
"""
Advent Of Code 2022 Day 12
https://adventofcode.com/2022/day/12
"""
from collections import deque
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
        with open(filename) as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line.strip()):
                    self.grid[x, y] = self.fix_elevation(char)
                    if char == "S":
                        self.start = x, y
                        self.aas.append((x, y))
                    elif char == "E":
                        self.end = x, y
                    elif char == "a":
                        self.aas.append((x, y))
                    self.max_x = max(self.max_x, x + 1)  # eh :(, could be fixed
                self.max_y = max(self.max_y, y + 1)  # same

    def fix_elevation(self, letter):
        if letter == "S":
            return "a"
        elif letter == "E":
            return "z"
        return letter

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

    def get_neighbors(self, loc):
        x, y = loc
        height = ord(self.grid[x, y])
        for (xx, yy) in self.get_raw_neighbors(x, y):
            this_height = ord(self.grid[xx, yy])
            if this_height <= (height + 1):
                yield xx, yy

    def get_neighbors_p2(self, loc):
        """for running backwards"""
        x, y = loc
        height = ord(self.grid[x, y])
        for (xx, yy) in self.get_raw_neighbors(x, y):
            this_height = ord(self.grid[xx, yy])
            if height <= (this_height + 1):
                yield xx, yy

    def bfs(self):  # -> (int | None):
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

    def bfs_p2(self):  # -> (int | None):
        """bfs backwards from end point to first 'a' encountered"""
        if self.end is None:
            return None

        init = State(self.end, 0)
        queue = deque([init])
        visited = set()
        while queue:
            state = queue.popleft()

            if state.loc in visited:
                continue
            visited.add(state.loc)

            if self.grid[state.loc] == "a":
                return state.steps

            for loc in self.get_neighbors_p2(state.loc):
                if loc not in visited:
                    queue.append(State(loc, state.steps + 1))

        return None


class Day12:
    """AoC 2022 Day 12"""

    @staticmethod
    def part1(filename: str):  # -> (int | None):
        g = Grid()
        g.parse(filename)
        return g.bfs()

    @staticmethod
    def part2(filename: str):  # -> (int | None):
        g = Grid()
        g.parse(filename)
        return g.bfs_p2()
