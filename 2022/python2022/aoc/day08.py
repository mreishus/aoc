#!/usr/bin/env python
"""
Advent Of Code 2022 Day 08
https://adventofcode.com/2022/day/8
"""


class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0

    def parse(self, filename: str):
        self.max_x = 0
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[x, y] = int(char)
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def is_edge(self, x, y):
        return x == 0 or y == 0 or x == (self.max_x - 1) or y == (self.max_y - 1)

    def is_visible(self, x, y):
        if self.is_edge(x, y):
            return True

        h = self.grid[x, y]
        generators = [self.gen_down, self.gen_up, self.gen_right, self.gen_left]
        for gen in generators:
            visible = True
            for xx, yy in gen(x, y):
                if self.grid[xx, yy] >= h:
                    visible = False
                    break
            if visible:
                return True

        return False

    def score(self, x, y):
        if self.is_edge(x, y):
            return 0

        score = 1
        h = self.grid[x, y]

        generators = [self.gen_down, self.gen_up, self.gen_right, self.gen_left]
        for gen in generators:
            term = 0
            for xx, yy in gen(x, y):
                term += 1
                if self.grid[xx, yy] >= h:
                    break
            score *= term
        return score

    def gen_right(self, x, y):
        for xx in range(x + 1, self.max_x):
            yield xx, y

    def gen_left(self, x, y):
        for xx in range(x - 1, -1, -1):
            yield xx, y

    def gen_up(self, x, y):
        for yy in range(y - 1, -1, -1):
            yield x, yy

    def gen_down(self, x, y):
        for yy in range(y + 1, self.max_y):
            yield x, yy

    def count_visible(self):
        count = 0
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.is_visible(x, y):
                    count += 1
        return count

    def highest_score(self):
        max_score = 0
        for y in range(self.max_y):
            for x in range(self.max_x):
                max_score = max(max_score, self.score(x, y))
        return max_score


class Day08:
    """AoC 2022 Day 08"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.count_visible()

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.highest_score()
