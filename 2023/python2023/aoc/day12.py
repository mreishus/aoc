#!/usr/bin/env python
"""
Advent Of Code 2023 Day 12
https://adventofcode.com/2023/day/12
"""
import re
import random


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    grid, nums = line.split(" ")
    nums = tuple(list(map(int, nums.split(","))))
    return grid, nums


memo = {}


def process(line):
    grid, nums = line
    if len(nums) == 0:
        return 1

    if line in memo:
        return memo[line]

    count_of_qs = grid.count("?")
    if count_of_qs == 0:
        if is_valid(grid, nums):
            return 1
        else:
            return 0

    ## Help deal with long lines
    match = re.match(r"^(\.*?)(#+)[\.$]", grid)
    if match:
        first_hash = match.group(2)
        if len(first_hash) > nums[0]:
            return 0
        if len(first_hash) == nums[0]:
            length_of_full_match = match.end()
            new_line = grid[
                length_of_full_match:
            ]  # Slice from the end of the entire match
            return process((new_line, nums[1:]))

    # if random.random() < 0.0001:
    #     print(grid, nums)

    total_valid = 0

    sum_nums = sum(nums)
    count_of_hashes = grid.count("#")

    if count_of_hashes + count_of_qs < sum_nums:
        # print("   --- return early 1")
        return 0

    if not is_valid_definite_prefix(grid, nums):
        # print("   --- return early 2")
        return 0

    first_qi = grid.find("?")

    with_dot = grid[:first_qi] + "." + grid[first_qi + 1 :]
    total_valid += process((with_dot, nums))

    if count_of_hashes < sum_nums:
        with_hash = grid[:first_qi] + "#" + grid[first_qi + 1 :]
        total_valid += process((with_hash, nums))

    memo[line] = total_valid
    return total_valid


def is_valid(grid, nums):
    if sum(nums) != grid.count("#"):
        return False

    in_run = False
    l = 0
    new_nums_index = 0
    for c in grid:
        if c == ".":
            if in_run:
                if new_nums_index < len(nums) and l != nums[new_nums_index]:
                    return False
                new_nums_index += 1
                in_run = False
            l = 0
        if c == "#":
            if not in_run:
                in_run = True
            l += 1

    if in_run:
        if in_run and new_nums_index < len(nums) and l > nums[new_nums_index]:
            return False
        in_run = False

    return True


def is_valid_definite_prefix(grid, nums):
    in_run = False
    l = 0
    new_nums_index = 0

    for c in grid:
        # Stop at the first '?'
        if c == "?":
            break

        if c == ".":
            if in_run:
                if new_nums_index < len(nums) and l != nums[new_nums_index]:
                    return False
                new_nums_index += 1
                in_run = False
            l = 0
        elif c == "#":
            if not in_run:
                in_run = True
            l += 1

        if in_run and new_nums_index < len(nums) and l > nums[new_nums_index]:
            return False

    # potentially valid
    return True


class Day12:
    """AoC 2023 Day 12"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        total = 0
        for line in data:
            x = process(line)
            total += x
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        total = 0
        for line in data:
            grid, nums = line
            grid = "?".join([grid] * 5)
            nums = nums + nums + nums + nums + nums

            x = process((grid, nums))
            # print(x)
            total += x
        return total
