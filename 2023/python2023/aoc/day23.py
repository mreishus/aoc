#!/usr/bin/env python
"""
Advent Of Code 2023 Day 23
https://adventofcode.com/2023/day/23
"""
from collections import deque


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

    def display(self, visited=set()):
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

    def neighbors(self, x, y, is_part2=False):
        ## (part 1) For slope tiles, we can only move in the direction of the slope.
        if not is_part2:
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

    def compute_distances(self, is_part2=False):
        ## Find special points (start, end, any point with > 2 neighbors)
        special_points = []
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.grid[(x, y)] == "#":
                    continue
                if (
                    (x, y) == self.start
                    or (x, y) == self.end
                    or len(list(self.neighbors(x, y, is_part2=is_part2))) > 2
                ):
                    special_points.append((x, y))

        distances = {}
        for point in special_points:
            these_distances = self.bfs(point, special_points, is_part2=is_part2)
            distances[point] = these_distances
        return distances

    def bfs(self, start, special_points, is_part2=False):
        visited = set([start])
        q = [(start, 0, visited)]
        q = deque(q)
        distances = {}
        while len(q) > 0:
            (x, y), steps, visited = q.pop()
            if (x, y) in special_points and (x, y) != start:
                distances[(x, y)] = steps
                continue

            for loc in self.neighbors(x, y, is_part2=is_part2):
                if loc in visited:
                    continue
                q.append(
                    (
                        loc,
                        steps + 1,
                        visited | {loc},
                    )
                )
        return distances

    def dfs(self, start, distances):
        visited = set([start])
        q = [(start, 0, visited)]
        q = deque(q)
        max_steps = 0
        while len(q) > 0:
            (x, y), steps, visited = q.pop()
            if (x, y) == self.end:
                if steps > max_steps:
                    max_steps = steps
                continue

            for loc, distance in distances[(x, y)].items():
                if loc in visited:
                    continue
                q.append(
                    (
                        loc,
                        steps + distance,
                        visited | {loc},
                    )
                )
        return max_steps


class Day23:
    """AoC 2023 Day 23"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        distances = g.compute_distances()
        return g.dfs(g.start, distances)

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        distances = g.compute_distances(is_part2=True)
        return g.dfs(g.start, distances)
