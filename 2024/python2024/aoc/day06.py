#!/usr/bin/env python
"""
Advent Of Code 2024 Day 06
https://adventofcode.com/2024/day/6
"""
from collections import defaultdict


class Grid:
    def __init__(self):
        self.grid = {}
        self.grid = defaultdict(lambda: "Z", self.grid)
        self.max_x = 0
        self.max_y = 0
        self.guard = (-1, -1)
        self.guard_dir = "U"
        self.original_guard = (-1, -1)
        self.original_guard_dir = "U"
        self.infinite_loop = False
        self.seen = set()  # Locations we've been at
        self.seen_dir = set()  # Locations+Dirs we've been at

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[(x, y)] = char
                    if char == "^":
                        self.guard = (x, y)
                        self.guard_dir = "U"
                        self.original_guard = self.guard
                        self.original_guard_dir = self.guard_dir
                        self.grid[(x, y)] = "."
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)
        if self.guard == (-1, -1):
            raise ValueError(f"Could not find guard")
        self.seen.add(self.guard)
        self.seen_dir.add((self.guard, self.guard_dir))

    def reset(self):
        self.infinite_loop = False
        self.seen = set()
        self.seen_dir = set()
        self.guard = self.original_guard
        self.guard_dir = self.original_guard_dir

    def is_loop_obstacle_position(self, ox, oy):
        if self.grid[(ox, oy)] == "Z":
            return False
        if self.grid[(ox, oy)] == "#":
            return False
        if (ox, oy) == self.original_guard:
            return False

        self.reset()

        self.grid[(ox, oy)] = "#"
        while self.grid[self.guard] != "Z" and not self.infinite_loop:
            self.guard_step()
        self.grid[(ox, oy)] = "."  # undo modification

        return self.infinite_loop

    def guard_step(self):
        gx, gy = self.guard
        dx, dy = self.get_direction(self.guard_dir)
        nx, ny = gx + dx, gy + dy
        if self.grid[(nx, ny)] == "#":
            self.guard_dir = self.turn_right(self.guard_dir)
        else:
            self.guard = (nx, ny)
            if self.grid[(nx, ny)] == ".":
                if (self.guard, self.guard_dir) in self.seen_dir:
                    self.infinite_loop = True
                self.seen.add(self.guard)
                self.seen_dir.add((self.guard, self.guard_dir))

    def part1(self):
        while self.grid[self.guard] != "Z":
            self.guard_step()
        return len(self.seen)

    def part2(self):
        self.part1()
        part1_seen = self.seen.copy()

        # Only try putting an obstabcle where the guard walked in part1,
        # else he will never run into it
        c = 0
        for x, y in part1_seen:
            if self.is_loop_obstacle_position(x, y):
                c += 1
        return c

    def turn_right(self, direction):
        if direction == "R":
            return "D"
        elif direction == "L":
            return "U"
        elif direction == "D":
            return "L"
        elif direction == "U":
            return "R"
        else:
            raise ValueError(f"Unknown direction: {direction}")

    def get_direction(self, direction):
        if direction == "R":
            return 1, 0
        elif direction == "L":
            return -1, 0
        elif direction == "D":
            return 0, 1
        elif direction == "U":
            return 0, -1
        else:
            raise ValueError(f"Unknown direction: {direction}")


class Day06:
    """AoC 2024 Day 06"""

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
