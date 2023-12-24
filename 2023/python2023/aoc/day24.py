#!/usr/bin/env python
"""
Advent Of Code 2023 Day 24
https://adventofcode.com/2023/day/24
"""
import re
from typing import List
from z3 import Solver, Reals, sat, Ints


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    x, y, z, a, b, c = ints(line)
    return [[x, y, z], [a, b, c]]


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


class Day24:
    """AoC 2023 Day 24"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        mn = 7
        mx = 27
        if len(data) >= 100:
            mn = 200000000000000
            mx = 400000000000000

        total = 0
        solver = Solver()
        t1, t2 = Reals("t1 t2")
        for i in range(len(data)):
            [[x1, y1, z1], [a1, b1, c1]] = data[i]
            solver.add(t1 >= 0)
            solver.add(t2 >= 0)
            solver.add(x1 + t1 * a1 >= mn)
            solver.add(x1 + t1 * a1 <= mx)
            solver.add(y1 + t1 * b1 >= mn)
            solver.add(y1 + t1 * b1 <= mx)
            for j in range(i + 1, len(data)):
                # print(i, j)
                [[x2, y2, z2], [a2, b2, c2]] = data[j]

                solver.push()
                solver.add(x1 + t1 * a1 == x2 + t2 * a2)
                solver.add(y1 + t1 * b1 == y2 + t2 * b2)
                if solver.check() == sat:
                    total += 1
                solver.pop()
            solver.reset()
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        solver = Solver()

        x99, y99, z99 = Ints("x99 y99 z99")
        a99, b99, c99 = Ints("a99 b99 c99")
        t1, t2, t3 = Ints("t1 t2 t3")
        times = [t1, t2, t3]
        ## First 3 rocks only
        for i in range(3):
            t = times[i]
            [[x1, y1, z1], [a1, b1, c1]] = data[i]
            solver.add(t >= 0)
            solver.add(x99 + t * a99 == x1 + t * a1)
            solver.add(y99 + t * b99 == y1 + t * b1)
            solver.add(z99 + t * c99 == z1 + t * c1)
        if solver.check() == sat:
            model = solver.model()
            x = model[x99].as_long()
            y = model[y99].as_long()
            z = model[z99].as_long()
            return abs(x) + abs(y) + abs(z)
        return 0
