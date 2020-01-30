#!/usr/bin/env python
"""
Advent Of Code 2015 Day 17
https://adventofcode.com/2015/day/17
"""

from aoc.parsers import all_lines
import itertools


def all_combinations(xs):
    for i, _ in enumerate(xs, 1):
        yield from itertools.combinations(xs, i)


def part1(containers, target):
    return sum(1 for comb in all_combinations(containers) if sum(comb) == target)


def part2(containers, target):
    matching = [comb for comb in all_combinations(containers) if sum(comb) == target]
    smallest_len = len(min(matching, key=len))
    return sum(1 for comb in matching if len(comb) == smallest_len)


class Day17:
    """ AoC 2015 Day 17 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 17 part 1 """
        containers = [int(x) for x in all_lines(filename)]
        return part1(containers, 150)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 17 part 2 """
        containers = [int(x) for x in all_lines(filename)]
        return part2(containers, 150)
