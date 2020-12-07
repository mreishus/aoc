#!/usr/bin/env python
"""
Advent Of Code 2020 Day 5
https://adventofcode.com/2020/day/5
"""

import re


def parse(filename):
    with open(filename) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def parse_line(line):
    left = line[0:7]
    right = line[7:]
    return (left, right)


def get_row(pair):
    (left, right) = pair
    num = 0
    for char in left:
        num *= 2
        if char == "B":
            num += 1
    return num


def get_column(pair):
    (left, right) = pair
    num = 0
    for char in right:
        num *= 2
        if char == "R":
            num += 1
    return num


def get_id(line):
    return get_row(line) * 8 + get_column(line)


class Day05:
    """ AoC 2020 Day 05 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 05 part 1 """
        # pair = parse_line("FBFBBFFRLR")
        # row = get_row(pair)
        # col = get_column(pair)
        # idd = get_id(pair)
        # print(f"row {row} col {col} idd={idd}")

        data = parse(filename)
        highest_pair = max(data, key=get_id)
        return get_id(highest_pair)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 05 part 2 """
        data = parse(filename)
        highest_pair = max(data, key=get_id)
        lowest_pair = min(data, key=get_id)
        high_val = get_id(highest_pair)
        low_val = get_id(lowest_pair)

        seen_vals = set()
        for d in data:
            val = get_id(d)
            seen_vals.add(val)

        print(f"abc {low_val} {high_val}")

        for i in range(low_val, high_val):
            if i not in seen_vals:
                print(f"Missing: {i}")
        print("abc")

        return len(data)
