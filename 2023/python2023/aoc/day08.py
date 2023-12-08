#!/usr/bin/env python
"""
Advent Of Code 2023 Day 8
https://adventofcode.com/2023/day/8
"""
import re
import math


def parse(filename: str):
    with open(filename) as file:
        lines = file.readlines()
        header = lines.pop(0).strip()
        header = [0 if char == "L" else 1 for char in header]

        lines.pop(0)

        mapp = {}
        for line in lines:
            groups = re.match(r"(\w+) = \((\w+), (\w+)\)", line).groups()
            mapp[groups[0]] = [groups[1], groups[2]]
        return header, mapp


class Day08:
    """AoC 2023 Day 08"""

    @staticmethod
    def part1(filename: str) -> int:
        header, mapp = parse(filename)

        here = "AAA"
        steps = 0
        while True:
            for direction in header:
                here = mapp[here][direction]
                steps += 1
            if here == "ZZZ":
                break
        return steps

    @staticmethod
    def part2(filename: str) -> int:
        header, mapp = parse(filename)

        heres = [location for location in mapp.keys() if location[2] == "A"]

        periods = []
        for here in heres:
            steps = 0
            while True:
                for direction in header:
                    here = mapp[here][direction]
                    steps += 1
                if here[2] == "Z":
                    break
            periods.append(steps)
        return math.lcm(*periods)
