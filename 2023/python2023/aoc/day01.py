#!/usr/bin/env python
"""
Advent Of Code 2023 Day 1
https://adventofcode.com/2023/day/1
"""
from typing import List
import re


def parse(filename: str) -> List[str]:
    with open(filename) as file:
        lines = file.read().strip().split("\n")
        return lines


def digits_p1(s: str) -> List[int]:
    return list(map(int, re.findall(r"\d", s)))


def digits_p2(s: str) -> List[int]:
    parts = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", s)
    lookup = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    return list(map(int, map(lambda x: lookup.get(x, x), parts)))


class Day01:
    """AoC 2023 Day 01"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        total = 0
        for line in data:
            digits = digits_p1(line)
            a = (10 * digits[0]) + digits[-1]
            total += a
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        total = 0
        for line in data:
            digits = digits_p2(line)
            a = (10 * digits[0]) + digits[-1]
            total += a
        return total
