#!/usr/bin/env python

from collections import defaultdict
from aoc.computer import Computer, solve1
from aoc.day21 import Day21


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


if __name__ == "__main__":
    program = parse("../../21/input.txt")
    d21 = Day21(program)
    print("part 1")
    print(d21.part1())
    print("part 2")
    print(d21.part2())
