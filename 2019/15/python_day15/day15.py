#!/usr/bin/env python

# from aoc.computer import Computer
from aoc.day15 import Day15


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


if __name__ == "__main__":
    program = parse("../../15/input.txt")
    print("Part 1:")
    print(Day15.part1(program))
