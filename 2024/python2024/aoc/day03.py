#!/usr/bin/env python
"""
Advent Of Code 2024 Day 3
https://adventofcode.com/2024/day/3
"""
from typing import List
import re


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


class Day03:
    """AoC 2024 Day 03"""

    @staticmethod
    def part1(filename: str) -> int:
        with open(filename) as file:
            string = "".join(file.read().split())

        pattern = r"mul\(\d+,\d+\)"
        mult_instructions = re.findall(pattern, string)
        total = 0
        for instr in mult_instructions:
            args = ints(instr)
            total += args[0] * args[1]
        return total

    @staticmethod
    def part2(filename: str) -> int:
        with open(filename) as file:
            string = "".join(file.read().split())

        do_dont_pattern = r"(do\(\)|don\'t\(\))"
        data = re.split(do_dont_pattern, string)

        active = True
        total = 0
        pattern = r"mul\(\d+,\d+\)"
        for (
            input
        ) in (
            data
        ):  # input is either "do()", "don't()", or unparsed partially corrupted data
            if input == "don't()":
                active = False
            elif input == "do()":
                active = True
            elif active:
                mult_instructions = re.findall(pattern, input)
                for instr in mult_instructions:
                    args = ints(instr)
                    total += args[0] * args[1]

        return total
