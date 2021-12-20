#!/usr/bin/env python
"""
Advent Of Code 2021 Day 20
https://adventofcode.com/2021/day/20
"""
import numpy as np


def parse(filename: str):
    with open(filename) as file:
        (b1, b2) = file.read().strip().split("\n\n")
        b2 = b2.split("\n")

        b2_rows = []
        for line in b2:
            this_line = []
            for char in line:
                if char == "#":
                    this_line.append(1)
                elif char == ".":
                    this_line.append(0)
                else:
                    raise ValueError
            b2_rows.append(this_line)
            this_line = []

        return b1, b2_rows


def enhance(b1, A):
    output = []
    for b in np.lib.stride_tricks.sliding_window_view(A, (3, 3)):
        row = []
        for c in b:
            bitmask = c.flatten()
            number = bitmask.dot(2 ** np.arange(bitmask.size)[::-1])
            value = b1[number]
            if value == "#":
                row.append(1)
            elif value == ".":
                row.append(0)
        output.append(row)

    return np.array(output)


class Day20:
    """ AoC 2021 Day 20 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 20 part 1 """
        b1, b2 = parse(filename)
        b2 = np.array(b2, dtype=np.int16)
        b2 = np.pad(b2, (100, 100), "constant", constant_values=(0, 0))
        b2 = enhance(b1, b2)
        b2 = enhance(b1, b2)
        return np.count_nonzero(b2)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 20 part 2 """
        data = parse(filename)
        b1, b2 = parse(filename)
        b2 = np.array(b2, dtype=np.int16)

        # There's probably a faster solution here where I do something other
        # than add enough padding at the beginning to slowly get whittled away
        # after 50 iterations. Each iteration reduces the size by 2x2
        b2 = np.pad(b2, (100, 100), "constant", constant_values=(0, 0))
        for _ in range(50):
            b2 = enhance(b1, b2)
        return np.count_nonzero(b2)
