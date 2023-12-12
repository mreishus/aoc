#!/usr/bin/env python
"""
Advent Of Code 2023 Day 11
https://adventofcode.com/2023/day/11
"""
from typing import List
from collections import defaultdict, namedtuple
from aoc.heapdict import heapdict

Move = namedtuple("Move", ("loc", "distance"))


class Grid:
    def __init__(self):
        self.grid = {}
        self.grid = defaultdict(lambda: ".", self.grid)

        self.max_x = 0
        self.max_y = 0
        self.galaxies = []
        self.galaxy_lookup = {}
        self.galaxy_cache = {}
        self.part2_mode = False

    def parse(self, filename: str):
        x = 0
        y = 0

        xs_with_galaxies = []
        ys_with_galaxies = []

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[(x, y)] = char
                    if char == "#":
                        xs_with_galaxies.append(x)
                        ys_with_galaxies.append(y)
                        self.galaxies.append((x, y))
                        self.galaxy_lookup[(x, y)] = len(self.galaxies) - 1
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

        self.expand_space(xs_with_galaxies, ys_with_galaxies)

    def expand_space(self, xs_with_galaxies, ys_with_galaxies):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.grid[(x, y)] == ".":
                    if x not in xs_with_galaxies or y not in ys_with_galaxies:
                        self.grid[(x, y)] = "2"

    def find_pathlen_between_galaxies(self, g_start, g_end):
        if (g_start, g_end) in self.galaxy_cache:
            # print(f"  ---> Found in cache: {self.galaxy_cache[(g_start, g_end)]}")
            return self.galaxy_cache[(g_start, g_end)]

        loc_start = self.galaxies[g_start]
        loc_end = self.galaxies[g_end]

        (x_start, y_start) = loc_start
        (x_end, y_end) = loc_end
        right_only = x_start < x_end
        up_only = y_start > y_end

        ### Dijkstra's
        dist_to = defaultdict(lambda: 999_999_999_999_999_999_999_999)
        # edge_to = {}
        open_set = heapdict()

        dist_to[loc_start] = 0
        open_set[loc_start] = 0
        while len(open_set) > 0:
            (loc, length) = open_set.popitem()

            if loc == loc_end:
                return length

            if self.grid[loc] == "#":
                g_here = self.galaxy_lookup[loc]
                self.galaxy_cache[(g_start, g_here)] = length
                self.galaxy_cache[(g_here, g_start)] = length

            moves = self.available_moves(loc, right_only, up_only)

            for move in moves:
                new_loc = move.loc
                if dist_to[new_loc] > dist_to[loc] + move.distance:
                    dist_to[new_loc] = dist_to[loc] + move.distance
                    # edge_to[new_loc] = move
                    open_set[new_loc] = dist_to[new_loc]

    def part1(self):
        total = 0
        i = 0
        for g_start in range(len(self.galaxies)):
            print(f"Starting at {g_start}")
            for g_end in reversed(range(g_start + 1, len(self.galaxies))):
                pathlen = self.find_pathlen_between_galaxies(g_start, g_end)
                # print(f"Pathlen from {g_start} to {g_end} is {pathlen}")
                total += pathlen
            i += 1
        return total

    def part2(self):
        self.part2_mode = True
        return self.part1()

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                print(self.grid[(x, y)], end="")
            print()

    def available_moves(self, loc, right_only=False, up_only=False):
        for x, y in self.get_neighbours(loc, right_only, up_only):
            if self.grid[(x, y)] == "2":
                distance = 2
                if self.part2_mode:
                    distance = 1000000
                yield Move((x, y), distance)
            else:
                yield Move((x, y), 1)

    def get_neighbours(self, loc, right_only=False, up_only=False):
        x, y = loc
        if x > 0 and not right_only:
            yield (x - 1, y)
        if x < self.max_x - 1 and right_only:
            yield (x + 1, y)
        if y > 0 and up_only:
            yield (x, y - 1)
        if y < self.max_y - 1 and not up_only:
            yield (x, y + 1)


class Day11:
    """AoC 2023 Day 11"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.part1()

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.part2()
