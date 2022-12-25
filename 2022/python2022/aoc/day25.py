#!/usr/bin/env python
"""
Advent Of Code 2022 Day 25
https://adventofcode.com/2022/day/25
"""


def parse(filename):
    with open(filename) as file:
        return [list(line.strip()) for line in file.readlines()]


def convert(num):
    x = 0
    for i, raw_digit in enumerate(reversed(num)):
        digit = 0
        if raw_digit.isdigit():
            digit = int(raw_digit)
        elif raw_digit == "-":
            digit = -1
        elif raw_digit == "=":
            digit = -2

        # term = 5**i * digit
        # print(f"{digit} * 5^{i} = {term}")
        x += 5**i * digit
    return x


def reverse_convert(num):
    if num == 0:
        return ""
    q = num // 5
    r = num % 5
    if r == 0:
        return reverse_convert(q) + "0"
    elif r == 1:
        return reverse_convert(q) + "1"
    elif r == 2:
        return reverse_convert(q) + "2"
    elif r == 3:
        q = (num + 2) // 5
        return reverse_convert(q) + "="
    elif r == 4:
        q = (num + 1) // 5
        return reverse_convert(q) + "-"
    return ""


class Day25:
    """AoC 2022 Day 25"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        total = 0
        for x in data:
            total += convert(x)
        return reverse_convert(total)
