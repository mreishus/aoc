#!/usr/bin/env python
"""
Advent Of Code 2023 Day 21
https://adventofcode.com/2023/day/21
"""
import re
from typing import List
from collections import defaultdict, deque
import time
import random


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

    def bfs(self, start=None, max_dist=6, extras=None):
        sizes = list(reversed(sorted(extras.keys())))
        if extras is None:
            extras = {}
        if start is None:
            start = self.start
        start = (start[0], start[1], 0, 0)
        visited = set()
        finish_locations = set()
        queue = deque([(start, 0)])
        i = 0
        while queue:
            i += 1
            loc, dist = queue.pop()
            if i % 500000 == 0:
                print(loc, dist, " | ", len(queue), len(visited), len(finish_locations))
            if (loc, dist) not in visited:
                visited.add((loc, dist))
                if dist == max_dist:
                    finish_locations.add(loc)

                if dist < max_dist:
                    (x, y, x_quot, y_quot) = loc

                    found_extra = False
                    for size in sizes:
                        this_extras = extras[size]
                        if (x, y) in this_extras and dist + size <= max_dist:
                            z = 0
                            for xx, yy, aa, bb in this_extras[(x, y)][0]:
                                new_loc = (xx, yy, x_quot + aa, y_quot + bb)
                                if (new_loc, dist + size) in visited:
                                    continue
                                queue.append((new_loc, dist + size))
                                z += 1
                            # print("Added", z, "extras using size", size)
                            found_extra = True
                            break

                    if not found_extra:
                        # print(f"No extras. dist={dist}, x={x}, y={y}")
                        # for size in sizes:
                        #     this_extras = extras[size]
                        #     print(this_extras.keys())
                        # if random.randint(0, 10) == 5 and max_dist > 100:
                        #     exit(1)
                        for n in self.get_neighbors(loc):
                            if (n, dist + 1) in visited:
                                continue
                            queue.append((n, dist + 1))
        self.visited = visited
        self.finish_locations = finish_locations
        return finish_locations, visited

    def get_neighbors(self, node):
        neighbors = []
        x, y, x_quot, y_quot = node
        possibilities = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        for xx, yy in possibilities:
            ## x wrap around: xx = xx % self.max_x
            ## y wrap around: yy = yy % self.max_y
            this_x_quot = x_quot
            this_y_quot = y_quot
            if xx < 0:
                this_x_quot -= 1
            elif xx >= self.max_x:
                this_x_quot += 1
            if yy < 0:
                this_y_quot -= 1
            elif yy >= self.max_y:
                this_y_quot += 1
            xx = xx % self.max_x
            yy = yy % self.max_y
            if (xx, yy) in self.grid and self.grid[(xx, yy)] != "#":
                neighbors.append((xx, yy, this_x_quot, this_y_quot))
        return neighbors


class Day21:
    """AoC 2023 Day 21"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        g.display()
        x = g.bfs(64)
        return len(x)

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        g.display()

        # The whole extras thing is not working out
        # how I thought it would. :(
        extras = {}
        for size in [
            10,
            30,
            50,
            70,
            90,
            110,
            130,
            150,
            170,
            190,
        ]:
            print("Computing extras for size", size)
            time_begin = time.time()
            if size not in extras:
                extras[size] = {}
            for y in range(g.max_y):
                print(f"row {y}")
                for x in range(g.max_x):
                    if g.grid[(x, y)] == ".":
                        here = g.bfs((x, y), size, extras=extras)
                        extras[size][(x, y)] = here
            time_end = time.time()
            print("  Time", time_end - time_begin)

        # print(extras.keys())
        print("Computing main")
        time_begin = time.time()
        z = g.bfs(None, 300, extras=extras)
        time_end = time.time()
        print("Time", time_end - time_begin)

        # 200 = 7 seconds
        # 300 = 25 seconds
        # 400 = 64 seconds
        return len(z[0])
