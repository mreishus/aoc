#!/usr/bin/env python
"""
Advent Of Code 2020 Day 15
https://adventofcode.com/2020/day/15
"""

def parse(filename):
    with open(filename) as f:
        first_line = f.readline()
        return [int(x) for x in first_line.split(",")]


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
        if last in said_p:
            last = said[last] - said_p[last]
        else:
            last = 0

        remember(last, i)

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
        return helper(data, 2020)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 15 part 2 """
        data = parse(filename)
        return helper(data, 30000000)
