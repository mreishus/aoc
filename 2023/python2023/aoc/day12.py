#!/usr/bin/env python
"""
Advent Of Code 2023 Day 12
https://adventofcode.com/2023/day/12
"""
import re
from typing import List
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    grid, nums = line.split(" ")
    nums = list(map(int, nums.split(",")))
    qis = []
    for i, c in enumerate(grid):
        if c == "?":
            qis.append(i)
    return grid, nums, qis


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def process(line):
    grid, nums, qis = line

    if len(qis) == 0:
        if is_valid(grid, nums):
            return 1
        else:
            return 0

    total_valid = 0

    first_qi = qis[0]
    with_dot = grid[:first_qi] + "." + grid[first_qi + 1 :]
    with_hash = grid[:first_qi] + "#" + grid[first_qi + 1 :]
    total_valid += process((with_dot, nums, qis[1:]))
    total_valid += process((with_hash, nums, qis[1:]))
    return total_valid


def is_valid(grid, nums):
    in_run = False
    l = 0
    new_nums = []
    for i, c in enumerate(grid):
        if c == ".":
            if in_run:
                if len(new_nums) >= len(nums) or l != nums[len(new_nums)]:
                    return False
                new_nums.append(l)
                in_run = False
            l = 0
        if c == "#":
            if not in_run:
                in_run = True
            l += 1
    if in_run:
        if len(new_nums) >= len(nums) or l != nums[len(new_nums)]:
            return False
        new_nums.append(l)
        in_run = False
    return new_nums == nums


class Day12:
    """AoC 2023 Day 12"""

    """
    . operational
    # damaged
    ? unknown
    """

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        total = 0
        for line in data:
            total += process(line)
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        print(data)
        return 1
