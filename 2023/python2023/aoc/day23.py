#!/usr/bin/env python
"""
Advent Of Code 2023 Day 23
https://adventofcode.com/2023/day/23
"""
import re
from typing import List
from collections import defaultdict, deque
from functools import lru_cache


class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.start = None
        self.end = None

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[(x, y)] = char
                    if char != "#" and self.start is None:
                        self.start = (x, y)
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

        ## Rescan the last row to find the end
        y = self.max_y - 1
        for x in range(self.max_x):
            if self.grid[(x, y)] != "#":
                self.end = (x, y)
                break

        # self.start, self.end = self.end, self.start

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) == self.start:
                    print("S", end="")
                elif (x, y) == self.end:
                    print("E", end="")
                else:
                    print(self.grid[(x, y)], end="")
            print()

    def display_with_visited(self, visited):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) == self.start:
                    print("S", end="")
                elif (x, y) == self.end:
                    print("E", end="")
                elif (x, y) in visited:
                    print("o", end="")
                else:
                    print(self.grid[(x, y)], end="")
            print()

    def find_path(self):
        visited = set(self.start)
        q = [
            (
                self.start,
                0,
                visited,
            )
        ]
        q = deque(q)
        winners = []
        max_winner = 0
        i = 0
        ns = {}
        while len(q) > 0:
            i += 1
            if i % 125000 == 0:
                i = 0
                print("Queue size: ", len(q))
            (x, y), steps, visited = q.pop()
            if (x, y) == self.end:
                if steps > max_winner:
                    winners.append((steps, visited))
                    max_winner = max(max_winner, steps)
                    print(
                        "Found a winner!",
                        steps,
                        "Max winner: ",
                        max_winner,
                    )
                continue

            ## Extra constraints.
            ## Never step on the same spot twice.
            ## (p1) If stepping on a slope tile, the next step must but in the given direction.
            if (x, y) not in ns:
                ns[(x, y)] = list(self.neighbors(x, y))
            # for loc in self.neighbors(x, y):
            for loc in ns[(x, y)]:
                if loc in visited:
                    continue

                prev = x, y
                to_add = set()
                inc = 1
                while loc in ns and len(ns[loc]) == 2:
                    ## pick the one that isn't the previous location
                    if ns[loc][0] == prev:
                        to_add.add(loc)
                        inc += 1
                        prev = loc
                        loc = ns[loc][1]
                    else:
                        to_add.add(loc)
                        inc += 1
                        prev = loc
                        loc = ns[loc][0]
                if loc in visited:
                    continue

                new_visited = visited | {loc} | to_add
                q.append(
                    (
                        loc,
                        steps + inc,
                        new_visited,
                    )
                )

        max_steps = max([steps for steps, visited in winners])
        print("Max steps: ", max_steps)
        for steps, visited in winners:
            print("Winner: ", steps)
        print("Max steps: ", max_steps)

    def neighbors(self, x, y):
        ## For slope tiles, we can only move in the direction of the slope.
        if self.grid[(x, y)] == ">":
            yield (x + 1, y)
            return
        elif self.grid[(x, y)] == "<":
            yield (x - 1, y)
            return
        elif self.grid[(x, y)] == "^":
            yield (x, y - 1)
            return
        elif self.grid[(x, y)] == "v":
            yield (x, y + 1)
            return

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            if x + dx < 0 or x + dx >= self.max_x:
                continue
            if y + dy < 0 or y + dy >= self.max_y:
                continue
            if self.grid[(x + dx, y + dy)] == "#":
                continue
            yield (x + dx, y + dy)


class Day23:
    """AoC 2023 Day 23"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        g.display()
        return g.find_path()

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        print(data)
        return 0
