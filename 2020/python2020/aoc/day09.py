#!/usr/bin/env python
"""
Advent Of Code 2020 Day 9
https://adventofcode.com/2020/day/9
"""


def parse(filename):
    with open(filename) as f:
        return [int(line.strip()) for line in f.readlines()]


def part1(nums, pre_size):
    i = 0
    k = pre_size

    def is_two_sum():
        target = nums[k]
        seen = set(nums[i:k])
        for x in nums[i:k]:
            other_num = target - x
            if other_num in seen:
                return True
        return False

    while k < len(nums):
        if not is_two_sum():
            return nums[k]
        i += 1
        k += 1
    return None


def part2(nums, pre_size):
    target = part1(nums, pre_size)

    i = 0
    j = 0
    s = nums[i]
    while i < len(nums) and j < len(nums):
        if s < target:
            j += 1
            s += nums[j]
        elif s > target:
            s -= nums[i]
            i += 1
        else:  # s == target
            return min(nums[i : j + 1]) + max(nums[i : j + 1])
    return None


class Day09:
    """ AoC 2020 Day 09 """

    @staticmethod
    def part1(filename: str, pre_size: int) -> int:
        """ Given a filename, solve 2020 day 09 part 1 """
        nums = parse(filename)
        return part1(nums, pre_size)

    @staticmethod
    def part2(filename: str, pre_size: int) -> int:
        """ Given a filename, solve 2020 day 09 part 2 """
        nums = parse(filename)
        return part2(nums, pre_size)
