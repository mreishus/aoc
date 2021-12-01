#!/usr/bin/env python
"""
Advent Of Code 2021 Day 1
https://adventofcode.com/2021/day/1
"""
from typing import List


def parse(filename: str) -> List[int]:
    with open(filename) as file:
        return [int(line.strip()) for line in file.readlines()]


class Day01:
    """ AoC 2021 Day 01 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 01 part 1 """
        data = parse(filename)
        last = -99
        count = 0
        for x in data:
            if x > last:
                count += 1
            last = x
        return count - 1

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 01 part 2 """
        data = parse(filename)
        last = -99
        count = 0
        i = 0
        j = 1
        while i < len(data):
            j = i + 3
            x = sum(data[i:j])
            if x > last:
                count += 1
            last = x
            i += 1
        return count - 1
