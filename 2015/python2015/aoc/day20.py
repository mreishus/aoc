#!/usr/bin/env python
"""
Advent Of Code 2015 Day 20
https://adventofcode.com/2015/day/20
"""

from aoc.parsers import first_line
import math


def sum_of_divisors(num):
    return sum(divisors(num))


def divisors(num):
    if num == 1:
        return [1]
    answer = [1, num]

    max_check = int(math.sqrt(num)) + 1
    for i in range(2, max_check):
        if num % i == 0:
            j = int(num / i)
            answer += [i, j]
    return answer


def part1(target):
    x = 200_000
    while True:
        if sum_of_divisors(x) * 10 >= target:
            return x
        x += 1


def part2(target):
    x = 200_000
    while True:
        if sum(d for d in divisors(x) if x / d <= 50) * 11 >= target:
            return x
        x += 1


class Day20:
    """ AoC 2015 Day 20 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 20 part 1 """
        target = int(first_line(filename))
        return part1(target)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 20 part 2 """
        target = int(first_line(filename))
        return part2(target)
