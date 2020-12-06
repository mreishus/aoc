#!/usr/bin/env python
"""
Advent Of Code 2020 Day 6
https://adventofcode.com/2020/day/6
"""

import re
from collections import Counter

def parse(filename):
    with open(filename) as file:
        # return [parse_line(line.strip()) for line in f.readlines()]
        lines = file.read().strip()
        groups = lines.split("\n\n")
        return groups

class Day06:
    """ AoC 2020 Day 06 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 04 part 1 """
        groups = parse(filename)

        answer = 0
        for group in groups:
            group = re.sub(r'\s+', '', group)
            answer += len(Counter(group))
        return answer

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 04 part 2 """
        groups = parse(filename)
        answer = 0
        for group in groups:
            group_size = group.count("\n") + 1
            group = re.sub(r'\s+', '', group)
            full_keys = [k for (k, v) in Counter(group).items() if v == group_size]
            answer += len(full_keys)
        return answer
