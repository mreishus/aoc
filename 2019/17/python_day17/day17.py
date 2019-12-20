#!/usr/bin/env python

from aoc.day17 import Day17Droid


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


if __name__ == "__main__":
    program = parse("../../17/input.txt")
    print("Part 1:")
    droid = Day17Droid(program)
    print("Part 1")
    print(droid.part1())

    print("Part 2")
    print(droid.part2())
