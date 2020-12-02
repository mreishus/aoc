#!/usr/bin/env python
"""
Advent Of Code 2020 Day 1
https://adventofcode.com/2020/day/1
"""
from typing import List, Optional


def parse(filename: str) -> List[str]:
    with open(filename) as file:
        return [int(line.strip()) for line in file.readlines()]


def find_target_multiply(data: List[int], i: int, j: int, target: int) -> Optional[int]:
    """
    Look for two numbers inside the data[i:j] array that sum up to target.
    Return those two numbers multiplied together if found.
    """
    nums_seen = set(data[i:j])
    for x in data[i:j]:
        sub_target = target - x
        if sub_target in nums_seen:
            return x * sub_target
    return None


class Day01:
    """ AoC 2020 Day 01 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 01 part 1 """
        data = parse(filename)
        return find_target_multiply(data, 0, len(data), 2020)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 01 part 2 """
        data = parse(filename)
        for i, v in enumerate(data):
            maybe_answer = find_target_multiply(data, i, len(data), 2020 - v)
            if maybe_answer is not None:
                return maybe_answer * v
        return None


##############
# 100 200 300 400 500 600 700 800 900 1000
#  ^   |--------------------------------|
# outer i=0, v=100,  inner i, j define the rest of the array
# I need 2020.  But I already have 100, and I have a quick solution for finding
# 2 numbers that add up to 2020.  So, instead, try to find 2020 - 100, or 1920, in the rest
# of the array.  If I can find 1920 with two other numbers later, then juts add 100 to it.

# 100 200 300 400 500 600 700 800 900 1000
#  ^   |--------------------------------|
#      ^   |----------------------------|
#          ^   |------------------------|
#              ^   |--------------------|
