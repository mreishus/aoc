#!/usr/bin/env python
"""
Advent Of Code 2023 Day 23
https://adventofcode.com/2023/day/23
"""
import re
from typing import List
from collections import defaultdict, deque


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
        # seen = set()
        winners = []
        while len(q) > 0:
            # print(len(q))
            (x, y), steps, visited = q.popleft()
            if (x, y) == self.end:
                print("Found a winner!", steps)
                winners.append((steps, visited))
                continue
                # self.display_with_visited(visited)
                # return steps
            # if (x, y) in seen:
            #     continue
            # seen.add((x, y))
            if self.grid[(x, y)] == "#":
                continue

            ## Extra constraints.
            ## Never step on the same spot twice.
            ## If stepping on a slope tile, the next step must but in the given direction.
            for loc in self.neighbors(x, y):
                if loc in visited:
                    continue
                new_visited = visited | {loc}
                q.append(
                    (
                        loc,
                        steps + 1,
                        new_visited,
                    )
                )

        for steps, visited in winners:
            print("Winner: ", steps)

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

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if abs(dx) + abs(dy) == 2:
                    continue
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
        return 0

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        print(data)
        return 0
