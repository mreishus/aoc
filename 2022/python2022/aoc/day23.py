#!/usr/bin/env python
"""
Advent Of Code 2022 Day 23
https://adventofcode.com/2022/day/23
"""
from collections import defaultdict, deque


def parse(filename):
    g = Grid()
    g.parse(filename)
    return g


class Grid:
    def __init__(self):
        self.grid = defaultdict(lambda: ".")
        self.max_x = 0
        self.max_y = 0
        self.directions = None
        self.deltas = None

    def parse(self, filename):
        with open(filename) as file:
            lines = file.read().strip().splitlines()
            self.max_y = len(lines)
            self.max_x = len(lines[0])
            for y, line in enumerate(lines):
                for x, c in enumerate(line):
                    self.grid[(x, y)] = c

    def get_neighbors_n(self, x, y):
        """Returns N, NE, NW"""
        return [
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y - 1),
        ]

    def get_neighbors_s(self, x, y):
        return [
            (x, y + 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
        ]

    def get_neighbors_e(self, x, y):
        return [
            (x + 1, y),
            (x + 1, y + 1),
            (x + 1, y - 1),
        ]

    def get_neighbors_w(self, x, y):
        return [
            (x - 1, y),
            (x - 1, y + 1),
            (x - 1, y - 1),
        ]

    def get_neighbors(self, x, y):
        return [
            (x, y + 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y - 1),
            (x + 1, y),
            (x - 1, y),
        ]

    def tick(self):
        moves = 0
        proposals = defaultdict(int)
        pd = {}

        if self.directions is None:
            self.directions = deque(["n", "s", "w", "e"])
        if self.deltas is None:
            self.deltas = deque([(0, -1), (0, 1), (-1, 0), (1, 0)])

        locs = list(self.grid.keys())
        for (x, y) in locs:
            if self.grid[(x, y)] == ".":
                continue

            ## If free, skip
            count = 0
            for (xx, yy) in self.get_neighbors(x, y):
                if self.grid[(xx, yy)] == "#":
                    count += 1
                    break
            if count == 0:
                continue

            counts = defaultdict(int)

            for (xx, yy) in self.get_neighbors_n(x, y):
                if self.grid[(xx, yy)] == "#":
                    counts["n"] += 1
            for (xx, yy) in self.get_neighbors_s(x, y):
                if self.grid[(xx, yy)] == "#":
                    counts["s"] += 1
            for (xx, yy) in self.get_neighbors_e(x, y):
                if self.grid[(xx, yy)] == "#":
                    counts["e"] += 1
            for (xx, yy) in self.get_neighbors_w(x, y):
                if self.grid[(xx, yy)] == "#":
                    counts["w"] += 1

            # print("")
            for d in self.directions:
                # print(f"[{x}, {y}] Examining {d} with {counts[d]}")
                if counts[d] == 0:
                    (xd, yd) = self.deltas[self.directions.index(d)]
                    proposals[(x + xd, y + yd)] += 1
                    pd[(x + xd, y + yd)] = (x, y)
                    break

        for (x, y) in proposals.keys():
            if proposals[(x, y)] == 1:
                frm = pd[(x, y)]
                self.grid[(x, y)] = "#"
                self.grid[frm] = "."
                moves += 1

        self.directions.rotate(-1)
        self.deltas.rotate(-1)
        return moves

    def display(self):
        for y in range(0, self.max_y):
            for x in range(0, self.max_x):
                print(self.grid[(x, y)], end="")
            print()

    def compute_elf_bounds(self):
        min_x = 100000
        max_x = -100000
        min_y = 100000
        max_y = -100000
        for (x, y) in self.grid.keys():
            if self.grid[(x, y)] == "#":
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
        return (min_x, max_x, min_y, max_y)

    def count_empty_tiles(self):
        (min_x, max_x, min_y, max_y) = self.compute_elf_bounds()
        count = 0
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if self.grid[(x, y)] == ".":
                    count += 1
        return count


class Day23:
    """AoC 2022 Day 23"""

    @staticmethod
    def part1(filename: str) -> int:
        g = parse(filename)
        # print(g.grid)
        # g.display()

        for _ in range(10):
            g.tick()
            # print("")
            # g.display()

        return g.count_empty_tiles()

    @staticmethod
    def part2(filename: str) -> int:
        g = parse(filename)
        i = 1
        while True:
            moved = g.tick()
            if moved == 0:
                break
            i += 1
        return i
