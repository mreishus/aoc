#!/usr/bin/env python
"""
Advent Of Code 2022 Day 24
https://adventofcode.com/2022/day/24
"""
from collections import defaultdict, deque
from functools import cache
from typing import NamedTuple

State = NamedTuple(
    "State",
    [("loc", tuple), ("minutes", int)],
)


class Grid:
    def __init__(self):
        self.grid = defaultdict(lambda: " ")
        self.max_x = 0
        self.max_y = 0
        self.init_blizzards = []
        self.start = None
        self.end = None

    def parse(self, filename):
        with open(filename) as file:
            lines = file.read().strip().splitlines()
            self.max_y = len(lines) - 1
            self.max_x = len(lines[0]) - 1
            for y, line in enumerate(lines):
                for x, c in enumerate(line):
                    if ["<", ">", "^", "v"].count(c) > 0:
                        self.init_blizzards.append((x, y, c))
                        self.grid[(x, y)] = "."
                    else:
                        self.grid[(x, y)] = c
                    if y == 0 and c == ".":
                        self.start = (x, y)
                    elif y == self.max_y and c == ".":
                        self.end = (x, y)
        self.init_blizzards = tuple(self.init_blizzards)

    @cache
    def advance_these_blizzards(self, blizzards):
        new_blizzards = []
        for x, y, d in blizzards:
            new_x, new_y = x, y
            if d == "<":
                new_x -= 1
                new_x %= self.max_x
                if new_x == 0:
                    new_x -= 1
                    new_x %= self.max_x
            elif d == ">":
                new_x += 1
                new_x %= self.max_x
                if new_x == 0:
                    new_x += 1
                    new_x %= self.max_x
            elif d == "^":
                new_y -= 1
                new_y %= self.max_y
                if new_y == 0:
                    new_y -= 1
                    new_y %= self.max_y
            elif d == "v":
                new_y += 1
                new_y %= self.max_y
                if new_y == 0:
                    new_y += 1
                    new_y %= self.max_y

            new_blizzards.append((new_x, new_y, d))
        return tuple(new_blizzards)

    @cache
    def blizzards_to_dct(self, blizzards):
        dct = defaultdict(list)
        for x, y, d in blizzards:
            dct[(x, y)].append(d)
        return dct

    @cache
    def blizzards_for_minute(self, minutes):
        if minutes == 0:
            return self.init_blizzards
        b = self.blizzards_for_minute(minutes - 1)
        return self.advance_these_blizzards(b)

    @cache
    def get_neighbors(self, loc, minutes):
        """Return neighbors, but I cannot move to blizzards."""
        next_blizzards = self.blizzards_for_minute(minutes + 1)
        dct = self.blizzards_to_dct(next_blizzards)
        neighbors = []
        for x, y in (
            (loc[0], loc[1]),
            (loc[0] + 1, loc[1]),
            (loc[0] - 1, loc[1]),
            (loc[0], loc[1] + 1),
            (loc[0], loc[1] - 1),
        ):
            if (x, y) not in dct and self.grid[(x, y)] == ".":
                neighbors.append((x, y))

        return neighbors

    def bfs(self, minutes=0):
        init = State(self.start, minutes)
        goal = self.end
        return self.bfs_(init, goal)

    def backwards_bfs(self, minutes=0):
        init = State(self.end, minutes)
        goal = self.start
        return self.bfs_(init, goal)

    def bfs_(self, init, goal):
        seen = set()
        queue = deque([init])
        i = 0
        while queue:
            loc, minutes = queue.popleft()
            if (loc, minutes) in seen:
                continue
            seen.add((loc, minutes))

            if i % 10000 == 0:
                print(
                    f"Seen {i} states | {len(queue)} in queue | {len(seen)} seen | loc {loc} | mins {minutes}"
                )
            i += 1

            if loc == goal:
                return minutes

            for n_loc in self.get_neighbors(loc, minutes):
                queue.append(State(n_loc, minutes + 1))

        return None

    def display(self, b, loc=None):
        dct = self.blizzards_to_dct(b)
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                if (x, y) == self.start:
                    print("S", end="")
                elif (x, y) == self.end:
                    print("E", end="")
                elif (x, y) == loc:
                    print("K", end="")
                elif (x, y) in dct:
                    if len(dct[(x, y)]) == 1:
                        print(dct[(x, y)][0], end="")
                    else:
                        print(len(dct[(x, y)]), end="")
                else:
                    print(self.grid[(x, y)], end="")
            print()


class Day24:
    """AoC 2022 Day 24"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        minutes = g.bfs()
        return minutes

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        minutes = g.bfs()
        minutes = g.backwards_bfs(minutes)
        minutes = g.bfs(minutes)
        return minutes
