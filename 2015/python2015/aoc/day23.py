#!/usr/bin/env python
"""
Advent Of Code 2015 Day 23
https://adventofcode.com/2015/day/23
"""


def simulate(initial_a):
    a = initial_a
    b = 0

    if a == 1:
        a *= 3
        a += 1
        a *= 3
        a += 1
        a += 1
        a *= 3
        a += 1
        a *= 3
        a += 1
        a += 1
        a *= 3
        a *= 3
        a += 1
        a += 1
        a *= 3
        a += 1
        a += 1
        a *= 3
        a += 1
        a += 1
        a *= 3
    else:
        a += 1
        a *= 3
        a += 1
        a *= 3
        a *= 3
        a *= 3
        a += 1
        a *= 3
        a += 1
        a *= 3
        a += 1
        a += 1
        a *= 3
        a *= 3
        a *= 3
        a += 1

    while True:
        if a == 1:
            return b
        b += 1
        if a % 2 == 0:
            a /= 2
        else:
            a *= 3
            a += 1
    return None


class Day23:
    """ AoC 2015 Day 23 """

    @staticmethod
    def part1(_filename: str) -> int:
        """ Given a filename, solve 2015 day 23 part 1 """
        return simulate(0)

    @staticmethod
    def part2(_filename: str) -> int:
        """ Given a filename, solve 2015 day 23 part 2 """
        return simulate(1)
