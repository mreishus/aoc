#!/usr/bin/env python
"""
Advent Of Code 2024 Day 14
https://adventofcode.com/2024/day/14
"""
from typing import List
import re
from collections import Counter, defaultdict

class Robot:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.max_x = 0
        self.max_y = 0

    def set_grid(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y

    def move(self, n):
        self.x = (self.x + n * self.vx) % self.max_x
        self.y = (self.y + n * self.vy) % self.max_y

    def quad(self):
        x_mid = self.max_x // 2
        y_mid = self.max_y // 2

        if self.x == x_mid or self.y == y_mid:
            return None

        if self.x < x_mid and self.y < y_mid:
            return 1
        elif self.x < x_mid and self.y > y_mid:
            return 2
        elif self.x > x_mid and self.y < y_mid:
            return 3
        elif self.x > x_mid and self.y > y_mid:
            return 4

def display(robots, max_x, max_y):
    grid = defaultdict(int)
    for r in robots:
        grid[r.x, r.y] += 1

    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in grid:
                print(grid[x, y], end="")
            else:
                print('.', end="")
            pass
        print("")

def has_line(robots, max_x, max_y, target):
    grid = defaultdict(int)
    for r in robots:
        grid[r.x, r.y] += 1

    for y in range(max_y):
        matcher = 0
        for x in range(max_x):
            if (x, y) in grid:
                matcher += 1
                if matcher >= target:
                    return True
            else:
                matcher = 0
            pass
    return False

def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

def parse(filename):
    with open(filename) as file:
        string = file.read().strip()
    data = []
    for line in string.split("\n"):
        [px, py, vx, vy] = ints(line)
        data.append(Robot(px, py, vx, vy))
    return data

class Day14:
    """AoC 2024 Day 14"""

    @staticmethod
    def part1(filename: str) -> int:
        robots = parse(filename)
        max_x = 101
        max_y = 103
        if (len(robots) < 20):
            max_x = 11
            max_y = 7

        quads = []
        for r in robots:
            r.set_grid(max_x, max_y)
            r.move(100)
            q = r.quad()
            if q is not None:
                quads.append(q)
        qc = Counter(quads)
        display(robots, max_x, max_y)

        safety = 1
        for c in qc.values():
            safety *= c
        return safety

    @staticmethod
    def part2(filename: str) -> int:
        robots = parse(filename)
        max_x = 101
        max_y = 103
        if (len(robots) < 20):
            max_x = 11
            max_y = 7

        for r in robots:
            r.set_grid(max_x, max_y)

        move_count = 0
        for i in range(200000):
            for r in robots:
                r.move(1)
            move_count += 1
            if has_line(robots, max_x, max_y, 10):
                break
        print("Matched at ", i)
        display(robots, max_x, max_y)
        print("Matched at ", i, move_count)

        return -1
