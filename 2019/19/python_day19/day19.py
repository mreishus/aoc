#!/usr/bin/env python

from collections import defaultdict
from aoc.computer import Computer, solve1
from aoc.day19 import Day19


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


if __name__ == "__main__":
    program = parse("../../19/input.txt")
    d9 = Day19(program)
    print("Part1")
    print(d9.part1())
    print("Part2")
    print(d9.part2())
