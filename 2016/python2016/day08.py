#!/usr/bin/env python
import numpy as np
import re


def parse(filename):
    """
    Input: string (filename)
    Output: List of (string, int, int) tuples (commands)
    Example output:
    [('RECT', 3, 2), ('RCOL', 1, 1), ('RROW', 0, 4), ('RCOL', 1, 1)]
    """
    commands = []

    rect_re = r"rect (\d+)x(\d+)"
    rrow_re = r"rotate row y=(\d+) by (\d+)"
    rcol_re = r"rotate column x=(\d+) by (\d+)"

    with open(filename) as file:
        for line in file:
            if re.match(rect_re, line):
                x, y = re.match(rect_re, line).groups()
                commands.append(("RECT", int(x), int(y)))
            elif re.match(rrow_re, line):
                y, amount = re.match(rrow_re, line).groups()
                commands.append(("RROW", int(y), int(amount)))
            elif re.match(rcol_re, line):
                x, amount = re.match(rcol_re, line).groups()
                commands.append(("RCOL", int(x), int(amount)))

    return commands


def part1(commands, xsize, ysize):
    grid = np.zeros((ysize, xsize), dtype=int)
    for (command, arg1, arg2) in commands:
        if command == "RECT":
            grid[:arg2, :arg1] = 1
        if command == "RROW":
            (index, amount) = (arg1, arg2)
            # Example: Roll the first row by two
            # a[1] = np.roll(a[1], 2)
            grid[index] = np.roll(grid[index], amount)
        if command == "RCOL":
            (index, amount) = (arg1, arg2)
            # Example: Roll the first col by one
            # grid[:, 1] = np.roll( grid[:, 1], 1)
            grid[:, index] = np.roll(grid[:, index], amount)

    return grid, np.count_nonzero(grid)


def part2(grid, xsize, ysize):
    for y in range(ysize):
        for x in range(xsize):
            if grid[y][x] == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print("")


if __name__ == "__main__":
    print("Part 1 Example:")
    commands_small = parse("../inputs/08/input_small.txt")
    grid, count = part1(commands_small, 7, 3)
    print(count)

    print("Part 1:")
    commands_small = parse("../inputs/08/input.txt")
    grid, count = part1(commands_small, 50, 6)
    print(count)

    print("Part 2:")
    part2(grid, 50, 6)
