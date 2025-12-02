#!/usr/bin/env python
"""
Advent Of Code 2025 Day 1
https://adventofcode.com/2025/day/1
"""

def parse(filename: str):
    r = []
    with open(filename) as file:
        lines = file.read().strip().split("\n")

    for line in lines:
        dir, num = line[0], line[1:]
        r.append( ( dir, int(num) ) )
    return r

def solve1(data):
    loc = 50
    zero_count = 0
    for (dir, steps) in data:
        if dir == 'R':
            loc = (loc + steps) % 100
        elif dir == 'L':
            loc = (loc - steps) % 100
        else:
            print("Bad location", loc)
            exit()
        if loc == 0:
            zero_count += 1
    return zero_count

def solve2(data):
    loc = 50
    zero_count = 0
    for (dir, steps) in data:
        if dir == 'R':
            for _ in range(steps):
                loc = (loc + 1) % 100
                if loc == 0:
                    zero_count += 1
        elif dir == 'L':
            for _ in range(steps):
                loc = (loc - 1) % 100
                if loc == 0:
                    zero_count += 1
        else:
            print("Bad location", loc)
            exit()
    return zero_count

class Day01:
    """AoC 2025 Day 01"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return solve1(data)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return solve2(data)
