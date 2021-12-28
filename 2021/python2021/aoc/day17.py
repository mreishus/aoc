#!/usr/bin/env python
"""
Advent Of Code 2021 Day 17
https://adventofcode.com/2021/day/17
"""
from typing import List
import re
from functools import lru_cache


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def parse(filename: str):
    with open(filename) as file:
        (a, b, c, d) = ints(file.read().strip())
        return Bound(a, b, c, d)


class Bound:
    def __init__(self, x, xx, y, yy):
        self.x = x
        self.xx = xx
        self.y = y
        self.yy = yy

    def is_range(self, this_x, this_y):
        return (
            self.x <= this_x
            and this_x <= self.xx
            and self.y <= this_y
            and this_y <= self.yy
        )


def whatever(bound, xv, yv):
    hit_target = False
    x = 0
    y = 0
    while True:
        x += xv
        y += yv
        if xv > 0:
            xv -= 1
        elif xv < 0:
            xv += 1
        yv -= 1
        if bound.is_range(x, y):
            hit_target = True
            break
        if yv < 0 and y < bound.y:
            break
        if xv == 0 and x < bound.x:
            break
    return hit_target


class Day17:
    """AoC 2021 Day 17"""

    @staticmethod
    @lru_cache(maxsize=None)
    def partX(filename: str):
        bound = parse(filename)

        total = 0
        max_y = 0

        lowest_x = 0
        for x in range(0, 500):
            if x * (x + 1) // 2 < bound.x:
                lowest_x = x
            else:
                break

        for x in range(lowest_x, bound.xx + 1):
            for y in range(bound.y, abs(bound.y)):
                hit_target = whatever(bound, x, y)
                if hit_target:
                    total += 1
                    max_y = max(max_y, y * (y + 1) // 2)

        return total, max_y

    @staticmethod
    def part1(filename: str) -> int:
        _, max_y = Day17.partX(filename)
        return max_y

    @staticmethod
    def part2(filename: str) -> int:
        total, _ = Day17.partX(filename)
        return total


if __name__ == "__main__":
    print(Day17.part2("/tmp/input_big.txt"))
