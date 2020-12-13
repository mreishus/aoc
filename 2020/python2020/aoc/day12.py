#!/usr/bin/env python
"""
Advent Of Code 2020 Day 12
https://adventofcode.com/2020/day/12
"""

import functools


def parse(filename):
    with open(filename) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def parse_line(line):
    (left, right) = line[0:1], line[1:]
    right = int(right)
    return (left, right)


def p1(data):
    # print("")
    d = complex(1, 0)
    loc = complex(0, 0)
    for (instruction, amount) in data:
        if instruction == "F":
            loc += d * amount
        elif instruction == "N":
            loc += complex(0, -1) * amount
        elif instruction == "S":
            loc += complex(0, 1) * amount
        elif instruction == "W":
            loc += complex(-1, 0) * amount
        elif instruction == "E":
            loc += complex(1, 0) * amount
        elif instruction == "L":
            turns = int(amount / 90)
            for z in range(turns):
                d *= -complex(0, 1)
        elif instruction == "R":
            turns = int(amount / 90)
            for z in range(turns):
                d *= complex(0, 1)
        # print(f"{loc} {d}")
    return int(abs(loc.real) + abs(loc.imag))


def p2(data):
    # print("")
    d = complex(1, 0)
    loc = complex(0, 0)
    way = complex(10, -1)
    for (instruction, amount) in data:
        # print(f" --> {instruction} {amount}")
        if instruction == "N":
            way += complex(0, -1) * amount
        elif instruction == "S":
            way += complex(0, 1) * amount
        elif instruction == "W":
            way += complex(-1, 0) * amount
        elif instruction == "E":
            way += complex(1, 0) * amount
        elif instruction == "F":
            diff = way - loc
            diff = complex(int(diff.real), int(diff.imag))
            loc += diff * amount
            way += diff * amount
        elif instruction == "L":
            diff = way - loc
            diff = complex(int(diff.real), int(diff.imag))
            turns = int(amount / 90)
            for z in range(turns):
                diff *= -complex(0, 1)
            way = diff + loc
        elif instruction == "R":
            diff = way - loc
            diff = complex(int(diff.real), int(diff.imag))
            turns = int(amount / 90)
            for z in range(turns):
                diff *= complex(0, 1)
            way = diff + loc
        # print(f"way={way} me={loc} {d}")
    return int(abs(loc.real) + abs(loc.imag))


class Day12:
    """ AoC 2020 Day 12 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 12 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 12 part 2 """
        data = parse(filename)
        return p2(data)
