#!/usr/bin/env python
"""
Advent Of Code 2021 Day 07
https://adventofcode.com/2021/day/7
"""
import numpy as np


def parse(filename: str):
    with open(filename) as file:
        return list(map(int, file.readline().strip().split(",")))


class Day07:
    """ AoC 2021 Day 07 """

    @staticmethod
    def part1(filename: str):
        """ Given a filename, solve 2021 day 07 part 1 """
        data = parse(filename)
        data = np.array(data)
        return min(sum(np.absolute(data - i)) for i in range(len(data)))

    @staticmethod
    def part2(filename: str):
        """ Given a filename, solve 2021 day 07 part 2 """
        data = np.array(parse(filename))

        def get_cost(a, i):
            b = np.absolute(a - i)
            return sum(b * (b + 1) / 2)

        return min(get_cost(data, i) for i in range(len(data)))
