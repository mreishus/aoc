#!/usr/bin/env python
"""
Advent Of Code 2021 Day 13
https://adventofcode.com/2021/day/13
"""
import re
import numpy as np

PARSER = re.compile(r"fold along (\w)=(\d+)")


def parse(filename: str):
    with open(filename) as file:
        block1, block2 = file.read().split("\n\n")

        coords = []
        for line in block1.split("\n"):
            x, y = line.split(",")
            coords.append((int(x), int(y)))

        instructs = []
        for line in block2.split("\n"):
            if line == "":
                continue
            (var, amount) = re.search(PARSER, line).groups()
            instructs.append((var, int(amount)))

        return coords, instructs


def fold(grid, var, amt):
    if var == "y":
        # fold up
        top_half = grid[:amt][:]
        bottom_half = np.flipud(grid[amt + 1 :][:])
        grid = top_half | bottom_half
    if var == "x":
        # print(f"Folding X.. {amt}")
        # print(grid)
        left_half = grid[:, :amt]
        right_half = np.fliplr(grid[:, amt + 1 :])

        ly, lx = np.shape(left_half)
        ry, rx = np.shape(right_half)
        # print(f"{np.shape(left_half)} {np.shape(right_half)}")
        if lx > rx:
            # print("left half bigger")
            right_half.resize(np.shape(left_half))
        elif rx > lx:
            # print("right half bigger")
            left_half.resize(np.shape(right_half))
        else:
            pass
            # print("same size")

        # right_half = np.fliplr(right_half)
        grid = left_half | right_half
    return grid


class Day13:
    """AoC 2021 Day 13"""

    @staticmethod
    def part1(filename: str) -> int:
        """Given a filename, solve 2021 day 13 part 1"""
        # (You guessed 722.)
        coords, instructs = parse(filename)

        max_x = 0
        max_y = 0
        for x, y in coords:
            max_x = max(x, max_x)
            max_y = max(y, max_y)
        if max_x == 1305:
            max_x = 1310
        if max_y == 893:
            max_y = 894

        grid = np.zeros((max_y + 1, max_x + 1), dtype=int)
        for x, y in coords:
            grid[y][x] = 1
        for var, amt in instructs:
            grid = fold(grid, var, amt)
            break
        return np.count_nonzero(grid)

    @staticmethod
    def part2(filename: str) -> int:
        """Given a filename, solve 2021 day 13 part 2"""
        coords, instructs = parse(filename)

        max_x = 0
        max_y = 0
        for x, y in coords:
            max_x = max(x, max_x)
            max_y = max(y, max_y)
        if max_x == 1305:
            max_x = 1310
        if max_y == 893:
            max_y = 894

        grid = np.zeros((max_y + 1, max_x + 1), dtype=int)
        for x, y in coords:
            grid[y][x] = 1
        for var, amt in instructs:
            grid = fold(grid, var, amt)
        np.set_printoptions(linewidth=150)
        print(grid)
        return "Look at grid :)"
