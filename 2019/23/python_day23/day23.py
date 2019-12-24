#!/usr/bin/env python

from collections import defaultdict, deque, Counter
from aoc.computer import Computer
from aoc.day23 import Day23


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


if __name__ == "__main__":
    program = parse("../../23/input.txt")
    d23 = Day23(program)
    p1, p2 = d23.execute()
    print("part 1")
    print(p1)
    print("part 2")
    print(p2)
