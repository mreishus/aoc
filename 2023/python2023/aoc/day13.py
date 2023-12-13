#!/usr/bin/env python
"""
Advent Of Code 2023 Day 13
https://adventofcode.com/2023/day/13
"""
import numpy as np


def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip()
        blocks = lines.split("\n\n")
        return [parse_block(block) for block in blocks]


def parse_block(block):
    grid = np.array([parse_line(x) for x in block.split("\n")])
    return grid


def parse_line(line: str):
    return [1 if char == "#" else 0 for char in line]


def find_reflections(block):
    ### First, look for vertical reflections.

    ## Draw a line between each pair of columns, then see if
    ## flipping the left side l-r matches the right side, after
    ## discarding any columns that don't overlap.

    for col in range(1, len(block[0])):
        left = np.fliplr(block[:, :col])
        right = block[:, col:]

        ## We need to find the larger out of left and right
        ## And then cut them down so they're the same size
        if left.shape[1] > right.shape[1]:
            left = left[:, : right.shape[1]]
        elif right.shape[1] > left.shape[1]:
            right = right[:, : left.shape[1]]

        if np.array_equal(left, right):
            # print("Found vertical reflection", col)
            return col

    ### Next, look for horizontal reflections.

    for row in range(1, len(block)):
        top = np.flipud(block[:row, :])
        bottom = block[row:, :]

        # print("")
        # print(f"--before shape-- {row}")
        # print(top)
        # print(bottom)
        ## We need to find the larger out of top and bottom
        ## And then cut them down so they're the same size
        if top.shape[0] > bottom.shape[0]:
            top = top[: bottom.shape[0], :]
        elif bottom.shape[0] > top.shape[0]:
            bottom = bottom[: top.shape[0], :]

        if np.array_equal(top, bottom):
            # print("Found horizontal reflection", row)
            return row * 100
    return 0


class Day13:
    """AoC 2023 Day 13"""

    @staticmethod
    def part1(filename: str) -> int:
        print(f"Day 13 Part 1: {filename}")
        data = parse(filename)
        total = 0
        for block in data:
            num = find_reflections(block)
            total += num
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        print(data)
        return -1
