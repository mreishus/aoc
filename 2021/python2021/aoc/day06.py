#!/usr/bin/env python
"""
Advent Of Code 2021 Day 06
https://adventofcode.com/2021/day/5
"""
from typing import List
from collections import deque, Counter, defaultdict

# import numpy as np


def parse(filename: str):
    with open(filename) as file:
        return list(map(int, file.readline().strip().split(",")))


class Day06:
    """ AoC 2021 Day 06 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 06 part 1 """
        data = parse(filename)
        data = deque(data)

        for _ in range(80):
            to_add = 0
            for i, x in enumerate(data):
                if x - 1 < 0:
                    data[i] = 6
                    to_add += 1
                else:
                    data[i] -= 1
            for _ in range(to_add):
                data.append(8)

        return len(data)

    @staticmethod
    def part2(filename: str) -> int:
        nums = defaultdict(int)
        data = parse(filename)
        for k, v in Counter(data).items():
            nums[k] = v

        for step in range(256):
            for i in range(-1, 8):
                nums[i] = nums[i + 1]
            nums[8] = nums[-1]
            nums[6] += nums[-1]
            nums[-1] = 0
            # print(f"{step+1} {sum(nums.values())}")
        return sum(nums.values())

    # @staticmethod
    # def part2_old(filename: str) -> int:
    #     """ Given a filename, solve 2021 day 06 part 2 """
    #     data = parse(filename)[0]
    #     data = np.array(data)

    #     for step in range(256):
    #         print(step)
    #         data -= 1
    #         to_add = np.count_nonzero(data == -1)
    #         print(f"{step} | Adding {to_add}")
    #         data = np.where(data == -1, 6, data)
    #         data = np.append(data, np.full((to_add), 8))

    #     print(data)
    #     print(f"Length is: {len(data)}")
