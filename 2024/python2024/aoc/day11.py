#!/usr/bin/env python
"""
Advent Of Code 2024 Day 11
https://adventofcode.com/2024/day/11
"""
from typing import List
import re
from functools import lru_cache

@lru_cache(maxsize=None)
def count_descendants(num, steps):
    if steps == 0:
        return 1

    if num == 0:
        return count_descendants(1, steps - 1)
    elif len(str(num)) % 2 == 0:
        s = str(num)
        mid = len(s)//2
        return (count_descendants(int(s[:mid]), steps - 1) +
                count_descendants(int(s[mid:]), steps - 1))
    else:
        return count_descendants(num * 2024, steps - 1)

def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

class Day11:
    """AoC 2024 Day 11"""

    @staticmethod
    def part1(filename: str) -> int:
        with open(filename) as file:
            string = file.read()
        stones = ints(string)

        total = 0
        for stone in stones:
            total += count_descendants(stone, 25)
        return total

    @staticmethod
    def part2(filename: str) -> int:
        with open(filename) as file:
            string = file.read()
        stones = ints(string)

        total = 0
        for stone in stones:
            total += count_descendants(stone, 75)
        return total
