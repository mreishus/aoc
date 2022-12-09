#!/usr/bin/env python
"""
Advent Of Code 2022 Day 09
https://adventofcode.com/2022/day/9
"""


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    direc, num = line.split(" ")
    return [direc, int(num)]


class Rope:
    def __init__(self, num):
        self.k = []  # Knot locations, head is k[0] and tail is k[-1]
        self.seen = set()
        for _ in range(num):
            self.k.append((0, 0))

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
        # Move head
        self.k[0] = (self.k[0][0] + dx, self.k[0][1] + dy)

        for i in range(1, len(self.k)):
            # Move knot i
            mx, my = self.compute_tail_move(i)
            self.k[i] = (self.k[i][0] + mx, self.k[i][1] + my)

        # print(f"Marking {self.k[-1]} as visited. Head is {self.k[0]}")
        self.seen.add(self.k[-1])

    def compute_tail_move(self, i):
        hx, hy = self.k[i - 1]
        tx, ty = self.k[i]
        dx = hx - tx
        dy = hy - ty

        touching = abs(dx) <= 1 and abs(dy) <= 1
        if touching:
            return 0, 0

        mx, my = 0, 0
        if dx > 0:
            mx += 1
        elif dx < 0:
            mx -= 1

        if dy > 0:
            my += 1
        elif dy < 0:
            my -= 1
        return mx, my

    def get_tail_visited(self):
        return len(self.seen)


class Day09:
    """AoC 2022 Day 09"""

    @staticmethod
    def part1(filename: str) -> int:
        directions = parse(filename)
        g = Rope(2)
        g.do_moves(directions)
        return g.get_tail_visited()

    @staticmethod
    def part2(filename: str) -> int:
        directions = parse(filename)
        g = Rope(10)
        g.do_moves(directions)
        return g.get_tail_visited()
