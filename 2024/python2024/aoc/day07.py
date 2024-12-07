#!/usr/bin/env python
"""
Advent Of Code 2024 Day 07
https://adventofcode.com/2024/day/7
"""
from typing import List
import re
from collections import deque


def parse(filename):
    data = []
    with open(filename) as file:
        for line in file:
            test_value, *rest = ints(line)
            data.append((test_value, rest))
    return data

def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

def myconcat(a, b):
    blen = len(str(b))
    return (a * (10 ** blen)) + b

def dfs(start, goal, is_p2=False):
    q = [start]
    q = deque(q)
    solution = False
    while len(q) > 0:
        nums = q.pop()

        if len(nums) == 1 and nums[0] == goal:
            solution = True
            break

        if len(nums) > 1:
            ## Can "+"
            new_nums = [ nums[0] + nums[1] ] + nums[2:]
            q.append(
                new_nums
            )
            ## Can "*"
            new_nums = [ nums[0] * nums[1] ] + nums[2:]
            q.append(
                new_nums,
            )
            if is_p2:
                ## Can "||"
                new_nums = [ myconcat( nums[0], nums[1] ) ] + nums[2:]
                q.append(
                    new_nums,
                )
    return solution


class Day07:
    """AoC 2024 Day 07"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        count = 0
        for (test_value, nums) in data:
            sol = dfs(nums, test_value)
            if sol:
                count += test_value
        return count

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        count = 0
        for (test_value, nums) in data:
            sol = dfs(nums, test_value, is_p2=True)
            if sol:
                count += test_value
        return count
