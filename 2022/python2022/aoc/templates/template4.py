#!/usr/bin/env python
"""
Advent Of Code 2022 Day 03
https://adventofcode.com/2022/day/3
"""
from typing import List
import heapq
import re

PARSER = re.compile(r"thing (\d+),(\d+), stuff")


def parse_block(block: str) -> int:
    """
    param block: '1000\n2000\n3000'
    return: 6000
    """
    return sum(int(line) for line in block.splitlines())


def parse(filename: str) -> List[int]:
    with open(filename) as file:
        return [int(line.strip()) for line in file.readlines()]


def parse2(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    return line.split(")")


def parse_line2(line):
    (x, y) = re.search(PARSER, line).groups()
    return (x, y)


def parse3(filename: str) -> List[int]:
    """
    Parse the input file into a list of integers.
    Each integer is the sum of the numbers in a block.
    """
    with open(filename) as file:
        lines = file.read().strip()
        blocks = lines.split("\n\n")
        return [parse_block(block) for block in blocks]


class Day03:
    """AoC 2022 Day 03"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        if len(data) <= 20:
            print(data)
        return -1

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        if len(data) <= 20:
            print(data)
        return -2
