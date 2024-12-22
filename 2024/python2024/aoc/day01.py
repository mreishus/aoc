#!/usr/bin/env python
"""
Advent Of Code 2024 Day 1
https://adventofcode.com/2024/day/1
"""
from typing import List
import re
from collections import Counter


def parse(filename: str):
    out1 = []
    out2 = []
    with open(filename) as file:
        lines = file.read().strip().split("\n")
    for line in lines:
        a, b = line.split()
        out1.append(int(a))
        out2.append(int(b))
    return [out1, out2]


class Day01:
    """AoC 2024 Day 01"""

    @staticmethod
    def part1(filename: str) -> int:
        l1, l2 = parse(filename)
        l1 = sorted(l1)
        l2 = sorted(l2)
        total = 0
        for i, item1 in enumerate(l1):
            item2 = l2[i]
            distance = abs(item2 - item1)
            total += distance
        return total

    @staticmethod
    def part2(filename: str) -> int:
        l1, l2 = parse(filename)
        c2 = Counter(l2)
        simscore = 0
        for item1 in l1:
            count = c2[item1]
            simscore += item1 * count
        return simscore
