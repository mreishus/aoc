#!/usr/bin/env python
"""
Advent Of Code 2023 Day 14
https://adventofcode.com/2023/day/14
"""
import re
from typing import List
from collections import defaultdict


class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0

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

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                print(self.grid[(x, y)], end="")
            # print(f" Row number {y} ", end="")
            # print(f" Inverse row number {self.max_y - y} ", end="")
            print()

    def cycle(self):
        self.slide_north()
        self.slide_west()
        self.slide_south()
        self.slide_east()

    def slide_north(self):
        for y in range(self.max_y):
            if y == 0:
                continue
            for x in range(self.max_x):
                if self.grid[(x, y)] == "O":
                    xx = x
                    yy = y
                    while yy > 0 and self.grid[(xx, yy - 1)] == ".":
                        yy -= 1
                    self.grid[(x, y)] = "."
                    self.grid[(xx, yy)] = "O"

    def slide_south(self):
        for y in reversed(range(self.max_y)):
            if y == self.max_y:
                continue
            for x in range(self.max_x):
                if self.grid[(x, y)] == "O":
                    xx = x
                    yy = y
                    while yy < (self.max_y - 1) and self.grid[(xx, yy + 1)] == ".":
                        yy += 1
                    self.grid[(x, y)] = "."
                    self.grid[(xx, yy)] = "O"

    def slide_east(self):
        for x in reversed(range(self.max_x)):
            if x == self.max_x:
                continue
            for y in range(self.max_y):
                if self.grid[(x, y)] == "O":
                    xx = x
                    yy = y
                    while xx < (self.max_x - 1) and self.grid[(xx + 1, yy)] == ".":
                        xx += 1
                    self.grid[(x, y)] = "."
                    self.grid[(xx, yy)] = "O"

    def slide_west(self):
        for x in range(self.max_x):
            if x == 0:
                continue
            for y in range(self.max_y):
                if self.grid[(x, y)] == "O":
                    xx = x
                    yy = y
                    while xx > 0 and self.grid[(xx - 1, yy)] == ".":
                        xx -= 1
                    self.grid[(x, y)] = "."
                    self.grid[(xx, yy)] = "O"

    def get_load(self):
        load = 0
        for y in range(self.max_y):
            weight = self.max_y - y
            for x in range(self.max_x):
                if self.grid[(x, y)] == "O":
                    load += weight
        return load


class Day14:
    """AoC 2023 Day 14"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        print("")
        g.display()
        print("")
        g.slide_north()
        g.display()
        return g.get_load()

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        print("")
        g.display()
        print("")
        for i in range(1000000000):
            if i % 100000 == 0:
                print(f"Cycle {i}. Percent complete: {i/10000000}%")
            g.cycle()
        return g.get_load()
