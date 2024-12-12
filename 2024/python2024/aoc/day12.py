#!/usr/bin/env python
"""
Advent Of Code 2024 Day 12
https://adventofcode.com/2024/day/12
"""
from collections import deque, defaultdict

class Region:
    def __init__(self, grid, coords, letter=None):
        self.grid = grid
        self.coords = coords
        self.area = None
        self.perim = None
        self.sides = None
        self.letter = letter

    def compute(self):
        self.area = len(self.coords)
        p = 0

        tmp_sides = defaultdict(list)

        for (x, y) in self.coords:
            this_p = 0
            region_neighbors = list(self.grid.get_neighbors_same_letter(x, y))
            for (dx, dy, orient, side) in [
                (-1, 0, "vert", "left"),
                (1, 0, "vert", "right"),
                (0, -1, "horiz", "top"),
                (0, 1, "horiz", "bottom"),
            ]:
                if (x+dx, y+dy) not in region_neighbors:
                    this_p += 1
                    if orient == "vert":
                        key = (x+dx, side)
                        val = y
                    elif orient == "horiz":
                        key = (y+dy, side)
                        val = x
                    else:
                        raise ValueError()
                    tmp_sides[key].append(val)

            p += this_p
        self.perim = p
        self.sides = 0
        for nums in tmp_sides.values():
            nums = sorted(nums)
            self.sides += self.count_runs(nums)

    def count_runs(self, nums):
        if not nums:
            return 0

        runs = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i-1] + 1:
                runs += 1

        return runs


class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.regions = []
        self.is_in_region = {}

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[(x, y)] = char
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def get_neighbors(self, x, y):
        for (dx, dy) in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]:
            if (x + dx, y + dy) in self.grid:
                yield (x + dx, y + dy)

    def get_neighbors_same_letter(self, x, y):
        my_letter = self.grid[(x, y)]
        for xx, yy in self.get_neighbors(x, y):
            if self.grid[(xx, yy)] == my_letter:
                yield (xx, yy)

    def bfs(self, start_loc):
        queue = deque([
            start_loc
        ])
        visited = set()
        while queue:
            loc = queue.pop()
            (x, y) = loc

            if loc in visited:
                continue
            visited.add(loc)

            for xx, yy in self.get_neighbors_same_letter(x, y):
                queue.append( (xx, yy) )
        return visited

    def sum_regions(self, use_sides=False):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) not in self.is_in_region:
                    seen = self.bfs((x, y))

                    r = Region(self, seen)
                    r.compute()
                    self.regions.append(r)

                    for (xx, yy) in seen:
                        self.is_in_region[(xx, yy)] = True
        score = 0
        for r in self.regions:
            if use_sides:
                score += r.area * r.sides
            else:
                score += r.area * r.perim
        return score

    def part1(self):
        return self.sum_regions(use_sides=False)

    def part2(self):
        return self.sum_regions(use_sides=True)


class Day12:
    """AoC 2024 Day 12"""

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

