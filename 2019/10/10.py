#!/usr/bin/env python
from collections import Counter
from itertools import zip_longest
from fractions import Fraction


class Day01:
    """Main module for solving Day01."""

    def __init__(self, name):
        self.name = name
        self.zero = 0

    def add_one_class(self, input_val: int) -> int:
        """Add one to a number, and example of class function."""
        return input_val + 1 + self.zero


def parse(filename):
    return [parse_line(line.strip()) for line in open(filename).readlines()]


def parse_line(line):
    return list(line)


def display(grid):
    for row in grid:
        for char in row:
            print(char, end="")
        print("")


def part1(grid):
    display(grid)
    size_y = len(grid)
    size_x = len(grid[0])
    print(f"{size_x} x {size_y}")

    max_sight = 0
    max_x = 0
    max_y = 0
    for y in range(size_y):
        for x in range(size_x):
            seen = how_many_seen(grid, x, y)
            # print(f"x{x} y{y} seen {seen}")
            if seen > max_sight:
                max_sight = seen
                max_x = x
                max_y = y
    return max_x, max_y, max_sight


def how_many_seen(grid, x, y):
    if grid[y][x] == ".":
        return 0
    # Build Blocked dict
    size_y = len(grid)
    size_x = len(grid[0])
    blocked = {}
    for ax in range(size_x):
        for ay in range(size_y):
            if ax == x and ay == y:
                continue
            if grid[ay][ax] == ".":
                continue
            x_diff = ax - x
            y_diff = ay - y
            x_diff_scaled = x_diff
            y_diff_scaled = y_diff
            if x_diff == 0:
                if y_diff_scaled > 0:
                    y_diff_scaled = 1
                else:
                    y_diff_scaled = -1
            elif y_diff == 0:
                if x_diff_scaled > 0:
                    x_diff_scaled = 1
                else:
                    x_diff_scaled = -1
            else:
                slope1 = Fraction(x_diff, y_diff)
                slope2 = Fraction(y_diff, x_diff)
                if abs(slope1.numerator) < abs(x_diff):
                    x_diff_scaled = slope1.numerator
                    y_diff_scaled = slope1.denominator
                    # -2/-4 reduces to 1/2, we want it to be -1/-2
                    # if x_diff < 0 and y_diff < 0:
                    #     x_diff_scaled *= -1
                    #     y_diff_scaled *= -1
                elif abs(slope2.numerator) < abs(y_diff):
                    y_diff_scaled = slope1.numerator
                    x_diff_scaled = slope1.denominator
                    # if x_diff < 0 and y_diff < 0:
                    #     x_diff_scaled *= -1
                    #     y_diff_scaled *= -1
            if x_diff < 0 and x_diff_scaled > 0:
                x_diff_scaled *= -1
            if x_diff > 0 and x_diff_scaled < 0:
                x_diff_scaled *= -1
            if y_diff < 0 and y_diff_scaled > 0:
                y_diff_scaled *= -1
            if y_diff > 0 and y_diff_scaled < 0:
                y_diff_scaled *= -1

            # print(f"What does {ax} {ay} block?")
            # print(f"  [{x_diff} {y_diff}] -> [{x_diff_scaled} {y_diff_scaled}]")

            blocked_x = ax
            blocked_y = ay
            while True:
                blocked_x += x_diff_scaled
                blocked_y += y_diff_scaled
                if (
                    blocked_x >= size_x
                    or blocked_x <= -1
                    or blocked_y >= size_y
                    or blocked_y <= -1
                ):
                    break
                # print(f"   --> Blocked!: {blocked_x} {blocked_y}")
                blocked[(blocked_y, blocked_x)] = True

    count = 0
    for ax in range(size_x):
        for ay in range(size_y):
            if grid[ay][ax] != "#":
                continue
            if ax == x and ay == y:
                continue
            if (ay, ax) in blocked:
                # print(f"{ax} {ay} is BLOCKED")
                continue
            # print(f" See {ax} {ay}")
            count += 1

    return count


if __name__ == "__main__":
    ## WORKING
    grid = parse("./input_small.txt")
    (x, y, count) = part1(grid)
    assert x == 3
    assert y == 4
    assert count == 8

    ## WORKING
    grid = parse("./input_small2.txt")
    (x, y, count) = part1(grid)
    assert x == 5
    assert y == 8
    assert count == 33

    ## WORKING
    grid = parse("./input_small3.txt")
    (x, y, count) = part1(grid)
    assert x == 1
    assert y == 2
    assert count == 35

    ## WORKING
    grid = parse("./input_small4.txt")
    (x, y, count) = part1(grid)
    assert x == 6
    assert y == 3
    assert count == 41

    ## WORKING
    grid = parse("./input_small5.txt")
    (x, y, count) = part1(grid)
    assert x == 11
    assert y == 13
    assert count == 210

    # # print(part1(grid))
    # x = 11
    # y = 13
    # print(f"Let's examine {x} {y}!!!")
    # print(how_many_seen(grid, x, y))

    print("Part1: ")
    grid = parse("./input.txt")
    # You guessed 219.
    print(part1(grid))

    print("Part2: ")
    # print(solve(245182, 790572))
    # print(solve2(245182, 790572))
