#!/usr/bin/env python
"""
Advent Of Code 2025 Day 6
https://adventofcode.com/2025/day/6
"""

from operator import mul
from functools import reduce

def parse(filename: str):
    r = []
    with open(filename) as file:
        lines = file.read().strip().split("\n")
    for line in lines[: len(lines) - 1 ]:
        parts = line.split()
        parts = list(map(int, parts))
        r.append(parts)
    r.append(lines[-1].split())
    return r

def parse2(filename: str):
    with open(filename) as file:
        lines = file.read().strip().split("\n")
    return lines

def solve1(data):
    num = len(data[0])
    totals = []
    for i in range(num):
        total = 0
        nums = []
        for line in data[: len(data) - 1 ]:
            nums.append(line[i])
        if data[-1][i] == '+':
            total = sum(nums)
        elif data[-1][i] == '*':
            total = reduce(mul, nums, 1)
        else:
            print("Bad operator")
            exit()
        totals.append(total)
    return sum(totals)

def solve2(data):
    operators_line = data[-1]
    operators = operators_line.split()
    lines = data[: len(data) - 1 ]

    totals = []
    nums = []
    for i in reversed(range(len(lines[0]))):
        all_spaces = True
        num = ''
        for j in range(len(lines)):
            char = lines[j][i]
            if char != ' ':
                all_spaces = False
                num += char
        if num != '':
            num = int(num)
            nums.append(num)
        if all_spaces or i == 0:
            op = operators.pop()
            if op == '+':
                total = sum(nums)
            elif op == '*':
                total = reduce(mul, nums, 1)
            else:
                print("Bad operator")
                exit()
            totals.append(total)
            nums = []
    return sum(totals)


class Day06:
    """AoC 2025 Day 06"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return solve1(data)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse2(filename)
        return solve2(data)


