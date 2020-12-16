#!/usr/bin/env python
"""
Advent Of Code 2020 Day 15
https://adventofcode.com/2020/day/15
"""

from collections import defaultdict


def parse(filename):
    with open(filename) as f:
        first_line = f.readline()
        return [int(x) for x in first_line.split(",")]


def p1(data):
    return helper(data, 2020)


def p2(data):
    return helper(data, 30000000)


def helper(data, stop):
    # print(f"-- {data} |  {stop}")
    i = 0
    said = {}
    said_p = {}
    last = None

    def remember(val, i):
        if val in said:
            said_p[val] = said[val]
        said[val] = i

    while i < len(data):
        val = data[i]
        remember(val, i)
        last = val
        i += 1

    while i < stop:
        to_say = None
        if last in said and last in said_p:
            to_say = said[last] - said_p[last]
        else:
            to_say = 0

        remember(to_say, i)
        last = to_say
        # print(f"Saying {to_say})")

        i += 1
        # if i % 250000 == 0:
        #     print(round(i / 30000000 * 100))
    return last


class Day15:
    """ AoC 2020 Day 15 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 15 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 15 part 2 """
        data = parse(filename)
        return p2(data)
