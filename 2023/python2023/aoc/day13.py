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


def find_reflections(block, ignore_this=None):
    # vertical reflections
    for col in range(1, len(block[0])):
        left = np.fliplr(block[:, :col])
        right = block[:, col:]

        # reshape
        if left.shape[1] > right.shape[1]:
            left = left[:, : right.shape[1]]
        elif right.shape[1] > left.shape[1]:
            right = right[:, : left.shape[1]]

        if np.array_equal(left, right) and col != ignore_this:
            # print("Found vertical reflection", col)
            return col

    # horizontal reflections
    for row in range(1, len(block)):
        top = np.flipud(block[:row, :])
        bottom = block[row:, :]

        # reshape
        if top.shape[0] > bottom.shape[0]:
            top = top[: bottom.shape[0], :]
        elif bottom.shape[0] > top.shape[0]:
            bottom = bottom[: top.shape[0], :]

        if np.array_equal(top, bottom) and row * 100 != ignore_this:
            # print("Found horizontal reflection", row)
            return row * 100
    return 0


def find_smudge_reflections(block):
    original_num = find_reflections(block)

    for row in range(len(block)):
        for col in range(len(block[0])):
            smudged = block.copy()
            smudged[row][col] = 1 - smudged[row][col]

            num = find_reflections(smudged, original_num)
            if num != original_num and num != 0:
                return num

    return 0


class Day13:
    """AoC 2023 Day 13"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        total = 0
        for block in data:
            num = find_reflections(block)
            total += num
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        total = 0
        for block in data:
            num = find_smudge_reflections(block)
            total += num
        return total
