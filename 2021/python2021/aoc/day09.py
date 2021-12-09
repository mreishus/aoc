#!/usr/bin/env python
"""
Advent Of Code 2021 Day 09
https://adventofcode.com/2021/day/9
"""
import re
import math


def parse(filename: str):
    with open(filename) as file:
        grid = {}
        x = 0
        y = 0
        for line in file.readlines():
            line = line.strip()
            x = 0
            for char in line:
                grid[x, y] = int(char)
                x += 1
            y += 1
        return grid, x, y


def get_neighbors(x, y, x_size, y_size):
    cands = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    for (xx, yy) in cands:
        if xx >= 0 and xx < x_size and yy >= 0 and yy < y_size:
            yield xx, yy


def get_risk_points(grid, x_size, y_size):
    risk_points = []
    for y in range(y_size):
        for x in range(x_size):

            is_low = True
            for xx, yy in get_neighbors(x, y, x_size, y_size):
                if grid[xx, yy] <= grid[x, y]:
                    is_low = False
            if is_low:
                risk_points.append((x, y))
    return risk_points


class Day09:
    """ AoC 2021 Day 09 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 09 part 1 """
        grid, x_size, y_size = parse(filename)
        total_risk = 0
        for (x, y) in get_risk_points(grid, x_size, y_size):
            total_risk += grid[x, y] + 1
        return total_risk

    @staticmethod
    def part2(filename: str) -> int:
        grid, x_size, y_size = parse(filename)
        basins = []
        for x, y in get_risk_points(grid, x_size, y_size):
            this_basin = [(x, y)]
            queue = [(x, y)]
            while len(queue) > 0:
                x, y = queue.pop()
                for xx, yy in get_neighbors(x, y, x_size, y_size):
                    if (xx, yy) in this_basin:
                        continue
                    if grid[xx, yy] == 9 or grid[xx, yy] <= grid[x, y]:
                        continue
                    this_basin.append((xx, yy))
                    queue.append((xx, yy))
            basins.append(this_basin)
        bls = sorted([len(basin) for basin in basins])
        return math.prod(bls[-3:])
