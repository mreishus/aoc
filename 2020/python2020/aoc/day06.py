#!/usr/bin/env python
"""
Advent Of Code 2020 Day 6
https://adventofcode.com/2020/day/6
"""

import re
from collections import Counter


def parse(filename):
    with open(filename) as file:
        return file.read().strip().split("\n\n")


def remove_whitespace(x):
    return re.sub(r"\s+", "", x)


class Day06:
    """ AoC 2020 Day 06 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 04 part 1 """
        groups = parse(filename)

        return sum(len(set(remove_whitespace(g))) for g in groups)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 04 part 2 """
        groups = parse(filename)
        answer = 0
        for group in groups:
            group_size = group.count("\n") + 1
            for (_k, v) in Counter(remove_whitespace(group)).items():
                if v == group_size:
                    answer += 1
        return answer
