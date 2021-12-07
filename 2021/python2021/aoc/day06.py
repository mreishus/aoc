#!/usr/bin/env python
"""
Advent Of Code 2021 Day 06
https://adventofcode.com/2021/day/6
"""
from collections import Counter
import numpy as np
from numpy.linalg import matrix_power


def parse(filename: str):
    with open(filename) as file:
        return list(map(int, file.readline().strip().split(",")))


def step(a, count):
    m = np.array(
        [
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    m_power = matrix_power(m, count)
    # print(m_power)
    return np.matmul(m_power, a)


class Day06:
    """ AoC 2021 Day 06 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 06 part 1 """
        data = parse(filename)

        a = np.zeros(9)
        for k, v in Counter(data).items():
            a[k] = v

        a = step(a, 80)
        return int(np.sum(a))

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)

        a = np.zeros(9)
        for k, v in Counter(data).items():
            a[k] = v

        a = step(a, 256)
        return int(np.sum(a))
