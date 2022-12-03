#!/usr/bin/env python
"""
Advent Of Code 2022 Day 03
https://adventofcode.com/2022/day/3
"""


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    return list(line)  # .split("")


def letter_to_number(letter):
    if letter.isupper():
        return ord(letter) - ord("A") + 1 + 26
    return ord(letter) - ord("a") + 1


class Day03:
    """AoC 2022 Day 03"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        score = 0
        for sack in data:
            mid = len(sack) // 2
            left = set(sack[0:mid])
            right = set(sack[mid:])
            overlap = left.intersection(right)
            score += letter_to_number(overlap.pop())
        return score

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        score = 0
        while len(data):
            r1 = set(data.pop())
            r2 = set(data.pop())
            r3 = set(data.pop())
            overlap = r1.intersection(r2).intersection(r3)
            score += letter_to_number(overlap.pop())
        return score
