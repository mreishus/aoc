#!/usr/bin/env python
"""
Advent Of Code 2024 Day 2
https://adventofcode.com/2024/day/2
"""
from typing import List
import re
from collections import Counter


def parse(filename: str):
    out1 = []
    with open(filename) as file:
        lines = file.read().strip().split("\n")
    for line in lines:
        out1.append(ints(line))
    return out1

def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

def is_safe(level):
    direction = None
    last_seen = None
    for item in level:
        if last_seen is not None:
            diff = item - last_seen
            if diff == 0:
                return False

            this_direction = diff > 0
            if direction is not None and direction != this_direction:
                return False
            direction = this_direction

            if abs(diff) > 3:
                return False
        last_seen = item
    return True

def is_safe2(level):
    if is_safe(level):
        return True
    for i in range(len(level)):
        newlist = level[:i] + level[i+1:]
        if is_safe(newlist):
            return True
    return False


class Day02:
    """AoC 2024 Day 02"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        safe_count = 0
        for level in data:
            if is_safe(level):
                safe_count += 1
        return safe_count

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        safe_count = 0
        for level in data:
            if is_safe2(level):
                safe_count += 1
        return safe_count
