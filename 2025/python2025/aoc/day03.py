#!/usr/bin/env python
"""
Advent Of Code 2025 Day 3
https://adventofcode.com/2025/day/3
"""

def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip().split("\n")
    lines = [ list(map(int, list(x))) for x in lines]
    return lines

def solve1(data):
    total = 0
    for line in data:
        total += best2(line, 2)
    return total

def solve2(data):
    total = 0
    for line in data:
        total += best2(line, 12)
    return total

def best2(line, digits):
    rtn = 0
    left = 0
    while digits > 0:
        consider = line[left:len(line)+1-digits]
        index_max = left + max(range(len(consider)), key=consider.__getitem__)
        rtn = rtn * 10 + line[index_max]
        left = index_max+1
        digits -= 1
    return rtn


class Day03:
    """AoC 2025 Day 03"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return solve1(data)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return solve2(data)

