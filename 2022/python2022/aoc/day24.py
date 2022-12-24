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
    [("loc", tuple), ("blizzards", tuple), ("minutes", int)],
)


class Grid:
    def __init__(self):
        self.grid = defaultdict(lambda: " ")
        self.max_x = 0
        self.max_y = 0
        self.init_blizzards = []
        self.blizzards = []
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
                        self.blizzards.append((x, y, c))
                        self.init_blizzards.append((x, y, c))
                        self.grid[(x, y)] = "."
                    else:
                        self.grid[(x, y)] = c
                    if y == 0 and c == ".":
                        self.start = (x, y)
                    elif y == self.max_y and c == ".":
                        self.end = (x, y)

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

    def advance_blizzards(self):
        self.blizzards = self.advance_these_blizzards(self.blizzards)

    @cache
    def blizzards_to_dct(self, blizzards):
        dct = defaultdict(list)
        for x, y, d in blizzards:
            dct[(x, y)].append(d)
        return dct

    @cache
    def get_neighbors(self, loc, blizzards):
        """Return neighbors, but I cannot move to blizzards."""
        next_blizzards = self.advance_these_blizzards(blizzards)
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
                neighbors.append(((x, y), next_blizzards))

        # print("")
        # self.display(blizzards, loc)

        # print("Current Loc", loc)
        # print("Neighbors")
        # for n in neighbors:
        #     print(n[0])
        # print("Next Blizzards")
        # self.display(next_blizzards)
        # print("")
        return neighbors

    def init_state(self):
        return State(self.start, tuple(self.blizzards), 0)

    def bfs(self, b, minutes=0):
        init = State(self.start, b, minutes)
        goal = self.end
        return self.bfs_(init, goal)

    def backwards_bfs(self, b, minutes=0):
        init = State(self.end, b, minutes)
        goal = self.start
        return self.bfs_(init, goal)

    def bfs_(self, init, goal):
        seen = set()
        queue = deque([init])
        i = 0
        while queue:
            loc, blizzards, minutes = queue.popleft()
            if (loc, blizzards) in seen:
                continue
            seen.add((loc, blizzards))

            if i % 10000 == 0:
                print(
                    f"Seen {i} states | {len(queue)} in queue | {len(seen)} seen | loc {loc} | mins {minutes}"
                )
            i += 1

            if loc == goal:
                return loc, minutes, blizzards

            for n_loc, n_blizzards in self.get_neighbors(loc, blizzards):
                queue.append(State(n_loc, n_blizzards, minutes + 1))

        return None, None, None

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
        loc, minutes, blizzards = g.bfs(tuple(g.init_blizzards))
        return minutes

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        loc, minutes, blizzards = g.bfs(tuple(g.init_blizzards))
        loc, minutes, blizzards = g.backwards_bfs(blizzards, minutes)
        loc, minutes, blizzards = g.bfs(blizzards, minutes)
        return minutes
