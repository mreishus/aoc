#!/usr/bin/env python
"""
Advent Of Code 2021 Day 02
https://adventofcode.com/2021/day/2
"""
from typing import List


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    (d, amount) = line.split(" ")
    return (d, int(amount))


class Day02:
    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        loc = complex(0, 0)
        for (d, amount) in data:
            if d == "forward":
                loc += complex(amount, 0)
            elif d == "down":
                loc += complex(0, amount)
            elif d == "up":
                loc -= complex(0, amount)

        return int(loc.real * loc.imag)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)

        loc = complex(0, 0)
        aim = 0
        for (d, amount) in data:
            if d == "forward":
                loc += complex(amount, aim * amount)
            elif d == "down":
                aim += amount
            elif d == "up":
                aim -= amount

        return int(loc.real * loc.imag)
