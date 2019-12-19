#!/usr/bin/env python

# from aoc.computer import Computer
from aoc.day15 import Day15


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


if __name__ == "__main__":
    program = parse("../../15/input.txt")
    p1, p2 = Day15.part1_and_2(program)
    print("Part 1:")
    print(p1)
    print("Part 2:")
    print(p2)
