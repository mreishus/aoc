#!/usr/bin/env python
"""
Advent Of Code 2021 Day 07
https://adventofcode.com/2021/day/7
"""
import numpy as np
import math


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

        def get_cost(a, i):
            return np.absolute(a - i)

        # return min(sum(get_cost(data, i)) for i in range(len(data)))
        median = np.median(data)
        j, k = math.floor(median), math.ceil(median)
        return min(sum(get_cost(data, i)) for i in [j, k])

    @staticmethod
    def part2(filename: str):
        """ Given a filename, solve 2021 day 07 part 2 """
        data = np.array(parse(filename))

        def get_cost(a, i):
            b = np.absolute(a - i)
            return int(sum(b * (b + 1) / 2))

        # return min(get_cost(data, i) for i in range(len(data)))
        mean = np.mean(data)
        j, k = math.floor(mean), math.ceil(mean)
        return min(get_cost(data, i) for i in [j, k])
