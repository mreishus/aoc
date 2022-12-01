#!/usr/bin/env python
"""
Advent Of Code 2022 Day 1
https://adventofcode.com/2022/day/1
"""
from typing import List
import heapq


def parse(filename: str) -> List[int]:
    """
    Parse the input file into a list of integers.
    Each integer is the sum of the numbers in a block.
    """
    with open(filename) as file:
        lines = file.read().strip()
        blocks = lines.split("\n\n")
        return [parse_block(block) for block in blocks]


def parse_block(block: str) -> int:
    """
    param block: '1000\n2000\n3000'
    return: 6000
    """
    return sum(int(line) for line in block.splitlines())


class Day01:
    """AoC 2022 Day 01"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return max(data)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return sum(heapq.nlargest(3, data))
