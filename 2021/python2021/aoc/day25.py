#!/usr/bin/env python
"""
Advent Of Code 2021 Day 25
https://adventofcode.com/2021/day/25
"""
from collections import defaultdict


def parse(filename: str):
    grid = defaultdict(lambda: " ")
    x = y = 0
    max_x = 0
    max_y = 0
    with open(filename) as f:
        for line in f:
            for char in line.strip("\n"):
                grid[x, y] = char
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                x += 1
            y += 1
            x = 0
    return grid, max_x + 1, max_y + 1


def display(grid, xsize, ysize):
    for y in range(ysize):
        for x in range(xsize):
            print(grid[x, y], end="")
        print("")


def step(grid, xsize, ysize):
    moved = False

    # Right march
    delete = set()
    add = set()
    for y in range(ysize):
        for x in range(xsize):
            me = (x, y)
            there = ((x + 1) % xsize, y)
            if grid[me] == ">" and grid[there] == ".":
                delete.add(me)
                add.add(there)
    for (x, y) in delete:
        grid[x, y] = "."
    for (x, y) in add:
        grid[x, y] = ">"

    if len(delete) > 0 or len(add) > 0:
        moved = True

    # Down March
    delete = set()
    add = set()
    for y in range(ysize):
        for x in range(xsize):
            me = (x, y)
            there = (x, (y + 1) % ysize)
            if grid[me] == "v" and grid[there] == ".":
                delete.add(me)
                add.add(there)
    for (x, y) in delete:
        grid[x, y] = "."
    for (x, y) in add:
        grid[x, y] = "v"

    if len(delete) > 0 or len(add) > 0:
        moved = True

    return grid, moved


class Day25:
    """AoC 2021 Day 25"""

    @staticmethod
    def part1(filename: str) -> int:
        """Given a filename, solve 2021 day 25 part 1"""
        grid, xs, ys = parse(filename)
        i = 0
        while True:
            grid, moved = step(grid, xs, ys)
            i += 1
            if not moved:
                break
        return i

    @staticmethod
    def part2(filename: str) -> int:
        return -1
