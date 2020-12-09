#!/usr/bin/env python
"""
Advent Of Code 2020 Day 9
https://adventofcode.com/2020/day/9
"""


def parse(filename):
    with open(filename) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def parse_line(line):
    return int(line)


class XMAS:
    def __init__(self, nums, pre_size):
        self.nums = nums
        self.pre_size = pre_size
        self.i = 0
        self.j = pre_size - 1
        self.next = pre_size

    def reset(self):
        self.i = 0
        self.j = self.pre_size - 1
        self.next = self.pre_size

    def is_two_sum(self):
        nums, i, j = self.nums, self.i, self.j
        target = self.nums[self.next]
        nums_seen = set(nums[i : j + 1])

        for x in nums[i : j + 1]:
            sub_target = target - x
            if sub_target in nums_seen:
                return True
        return False

    def p1(self):
        while True:
            if not self.is_two_sum():
                return self.nums[self.next]
            self.i += 1
            self.j += 1
            self.next += 1
        return None

    def p2(self):
        def weakness(i, j):
            return min(self.nums[i : j + 1]) + max(self.nums[i : j + 1])

        target = self.p1()
        self.reset()
        for i in range(0, len(self.nums)):
            s = self.nums[i]
            for j in range(i + 1, len(self.nums)):
                s += self.nums[j]
                if s == target:
                    return weakness(i, j)
        return None


class Day09:
    """ AoC 2020 Day 09 """

    @staticmethod
    def part1(filename: str, pre_size: int) -> int:
        """ Given a filename, solve 2020 day 09 part 1 """
        nums = parse(filename)
        return XMAS(nums, pre_size).p1()

    @staticmethod
    def part2(filename: str, pre_size: int) -> int:
        """ Given a filename, solve 2020 day 09 part 2 """
        nums = parse(filename)
        return XMAS(nums, pre_size).p2()
