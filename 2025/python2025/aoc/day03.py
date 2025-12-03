#!/usr/bin/env python
"""
Advent Of Code 2025 Day 3
https://adventofcode.com/2025/day/3
"""

def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip().split("\n")
    lines = [ list(map(int, list(x))) for x in lines]
    return lines

def solve1(data):
    total = 0
    for line in data:
        total += best1(line)
    return total

def best1(line):
    print('---')
    print(line)
    all_but_last = line[:len(line)-1]

    index1_max = max(range(len(all_but_last)), key=all_but_last.__getitem__)
    print(index1_max, all_but_last[index1_max])

    left = line[index1_max+1:]
    index2_max_left = max(range(len(left)), key=left.__getitem__)
    index2_max = index2_max_left + index1_max + 1

    return 10 * line[index1_max] + line[index2_max]


def solve2(data):
    return -1

class Day03:
    """AoC 2025 Day 03"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        print(data)
        return solve1(data)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return solve2(data)

