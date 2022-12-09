#!/usr/bin/env python
"""
Advent Of Code 2022 Day 09
https://adventofcode.com/2022/day/3
"""
from collections import defaultdict


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    direc, num = line.split(" ")
    return [direc, int(num)]


class Grid:
    def __init__(self):
        self.grid = defaultdict(int)
        self.hx = 0
        self.hy = 0
        self.tx = 0
        self.ty = 0
        self.grid[(0, 0)] = 1

    def do_moves(self, directions):
        lookup = {
            "R": (1, 0),
            "L": (-1, 0),
            "U": (0, 1),
            "D": (0, -1),
        }
        for direc, num in directions:
            dx, dy = lookup[direc]
            for _ in range(num):
                self.move(dx, dy)

    def move(self, dx, dy):
        # print("")
        # print(f"Before move: ({self.hx}, {self.hy}) - ({self.tx}, {self.ty})")
        self.hx += dx
        self.hy += dy
        # print(f"Half move: ({self.hx}, {self.hy}) - ({self.tx}, {self.ty})")
        self.move_tail()
        # print(f"After move:  ({self.hx}, {self.hy}) - ({self.tx}, {self.ty})")

    def move_tail(self):
        dx = self.hx - self.tx
        dy = self.hy - self.ty

        touching = abs(dx) <= 1 and abs(dy) <= 1
        if touching:
            return

        if dx > 0:
            self.tx += 1
        elif dx < 0:
            self.tx -= 1

        if dy > 0:
            self.ty += 1
        elif dy < 0:
            self.ty -= 1

        self.grid[(self.tx, self.ty)] = 1

    def get_tail_visited(self):
        count = 0
        for x in self.grid.keys():
            if self.grid[x] == 1:
                count += 1
        return count


class Day09:
    """AoC 2022 Day 09"""

    @staticmethod
    def part1(filename: str) -> int:
        directions = parse(filename)
        g = Grid()
        g.do_moves(directions)
        return g.get_tail_visited()

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        if len(data) <= 20:
            print(data)
        return -2
