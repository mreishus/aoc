#!/usr/bin/env python
"""
Advent Of Code 2024 Day 13
https://adventofcode.com/2024/day/13
"""
from typing import List
import re
# from z3 import Optimize, sat, Ints, Or

class Machine:
    def __init__(self, ax, ay, bx, by, px, py):
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.px = px
        self.py = py

    # def solve_alt(self):
    #     opt = Optimize()
    #     pressA, pressB = Ints("pressA pressB")
    #
    #     opt.add(pressA * self.ax + pressB * self.bx == self.px)
    #     opt.add(pressA * self.ay + pressB * self.by == self.py)
    #
    #     cost = pressA * 3 + pressB * 1
    #     opt.minimize(cost)
    #
    #     if opt.check() == sat:
    #         m = opt.model()
    #         return {
    #             'pressA': m[pressA].as_long(),
    #             'pressB': m[pressB].as_long(),
    #             'cost': m.eval(cost).as_long()
    #         }
    #     return None


    def solve(self):
        det = self.ax * self.by - self.bx * self.ay
        if det == 0:
            return None

        # cramer's rule
        pressA_float = (self.px * self.by - self.bx * self.py) / det
        pressB_float = (self.ax * self.py - self.px * self.ay) / det

        # if either number is more than 0.01 away from an integer, no solution
        fractA = abs(pressA_float - round(pressA_float))
        fractB = abs(pressB_float - round(pressB_float))
        if fractA > 0.01 or fractB > 0.01:
            return None

        pressA = round(pressA_float)
        pressB = round(pressB_float)

        # verify
        if (pressA * self.ax + pressB * self.bx == self.px and
            pressA * self.ay + pressB * self.by == self.py):
            return {
                'pressA': pressA,
                'pressB': pressB,
                'cost': 3 * pressA + pressB
            }
        return None

    def __str__(self):
        return f"#Machine({self.ax}, {self.ay})"
    def __repr__(self):
        return self.__str__()

def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

def parse(filename):
    with open(filename) as file:
        string = file.read()
    parts = string.split("\n\n")
    machines = []
    for p in parts:
        lines = p.split("\n")
        [ax, ay] = ints(lines[0])
        [bx, by] = ints(lines[1])
        [px, py] = ints(lines[2])
        machines.append( Machine( ax, ay, bx, by, px, py ) )
    return machines

class Day13:
    """AoC 2024 Day 13"""

    @staticmethod
    def part1(filename: str) -> int:
        machines = parse(filename)

        total = 0
        for m in machines:
            sol = m.solve()
            if sol is not None:
                total += sol['cost']
        return total

    @staticmethod
    def part2(filename: str) -> int:
        machines = parse(filename)

        total = 0
        for m in machines:
            m.px += 10000000000000
            m.py += 10000000000000

            sol = m.solve()
            if sol is not None:
                total += sol['cost']
        return total
