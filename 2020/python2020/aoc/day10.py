#!/usr/bin/env python
"""
Advent Of Code 2020 Day 10
https://adventofcode.com/2020/day/10
"""

import functools


def parse(filename):
    with open(filename) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def parse_line(line):
    return int(line)


def part1(data):
    voltages = set(data)
    highest = max(data)

    volts = 0
    d1 = 0
    d2 = 0
    d3 = 0
    while volts < highest:
        if (volts + 1) in voltages:
            d1 += 1
            volts += 1
            continue
        if (volts + 2) in voltages:
            d2 += 1
            volts += 2
            continue
        if (volts + 3) in voltages:
            d3 += 1
            volts += 3
            continue
    d3 += 1
    return d1 * d3


def part2(data):
    voltages = set(data)
    highest = max(data)

    @functools.cache
    def helper(v):
        if v == highest:
            return 1

        answer = 0
        for d in [1, 2, 3]:
            v_step = v + d
            if v_step not in voltages:
                continue
            answer += helper(v_step)
        return answer

    return helper(0)


class Day10:
    """ AoC 2020 Day 10 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 09 part 1 """
        data = parse(filename)
        return part1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 09 part 2 """
        data = parse(filename)
        return part2(data)
