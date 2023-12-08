#!/usr/bin/env python
"""
Advent Of Code 2023 Day 4
https://adventofcode.com/2023/day/4
"""
import re
from typing import List
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    _label, rest = line.split(":")
    winners, nums = rest.split("|")
    winners = ints(winners)
    nums = ints(nums)
    return winners, nums


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


class Day04:
    """AoC 2023 Day 04"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        total = 0
        for winners, nums in data:
            score = 0
            winners = set(winners)
            for num in nums:
                if num in winners:
                    if score == 0:
                        score = 1
                    else:
                        score *= 2

            total += score
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        total = 0
        i = 1
        copies = defaultdict(int)
        for winners, nums in data:
            offset = 1
            winners = set(winners)
            for num in nums:
                if num in winners:
                    copies[i + offset] += 1 + copies[i]
                    offset += 1
            i += 1

        total = 0
        ####### AHHHHH SPENT 10 MINUTES REALIZING I HAD TO ADD ,1 to enumerate
        for i, card in enumerate(data, 1):
            # print(i, card)
            total += 1 + copies[i]
        return total
        ## Incorrect Guess 1: 7641495
