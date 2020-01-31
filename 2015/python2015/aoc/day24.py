#!/usr/bin/env python
"""
Advent Of Code 2015 Day 24
https://adventofcode.com/2015/day/24
"""

from typing import List
from itertools import combinations
from functools import reduce
from operator import mul
from aoc.parsers import all_lines


def parse(filename: str) -> List[int]:
    return [int(x) for x in all_lines(filename)]


def part1(nums: List[int], num_groups: int) -> int:
    total = sum(nums)
    if total % num_groups > 0:
        raise ValueError("Expected sum of weights to be divisible by num_groups")
    target = total // num_groups

    # print(f"total={total} target={target}")
    sets = []
    for set_length in range(len(nums) // 3):
        # print(f"set length: {set_length} found so far: {len(sets)}")
        combs = [comb for comb in combinations(nums, set_length) if sum(comb) == target]
        sets.extend(combs)
    winner = min(sets, key=lambda s: reduce(mul, s))
    return reduce(mul, winner)


class Day24:
    """ AoC 2015 Day 24 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 24 part 1 """
        nums = parse(filename)
        return part1(nums, 3)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 24 part 2 """
        nums = parse(filename)
        return part1(nums, 4)
