#!/usr/bin/env python
"""
Advent Of Code 2024 Day 22
https://adventofcode.com/2024/day/22
"""
from collections import defaultdict
from typing import List
import re
from functools import lru_cache


def parse(filename):
    with open(filename) as file:
        string = file.read().strip()
    return list(map(int, string.split("\n")))


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def mix(num1, num2):
    return num1 ^ num2


def prune(num):
    return num % 16777216


def advance(num):
    num64 = num * 64
    num = mix(num64, num)
    num = prune(num)

    num32 = num // 32
    num = mix(num, num32)
    num = prune(num)

    num2k = num * 2048
    num = mix(num, num2k)
    num = prune(num)
    return num


def find_subsequence_index(A, B):
    len_a = len(A)
    len_b = len(B)

    # Iterate through B up to the point where A can fully fit
    for i in range(len_b - len_a + 1):
        # Check if the slice of B starting at i matches A
        if B[i : i + len_a] == A:
            return i  # Return the starting index

    return -1  # Return -1 if the subsequence is not found


class Day22:
    """AoC 2024 Day 22"""

    @staticmethod
    def part1(filename: str) -> int:
        buyers = parse(filename)
        total = 0
        for b in buyers:
            b0 = b
            for _ in range(2000):
                b = advance(b)
            total += b
        return total

    @staticmethod
    def part2(filename: str) -> int:
        buyers = parse(filename)
        total = 0
        print("\n")

        totals_for_window = defaultdict(int)
        for i, b in enumerate(buyers):
            window = []
            last_ones = None
            change = None
            changes = []
            prices = []
            seen = set()
            for _ in range(2001):
                ones = b % 10
                prices.append(ones)
                if last_ones is not None:
                    change = ones - last_ones
                    changes.append(change)
                    if len(window) < 4:
                        window.append(change)
                    else:
                        window = window[1:] + [change]

                    if len(window) == 4 and tuple(window) not in seen:
                        seen.add(tuple(window))
                        totals_for_window[tuple(window)] += ones
                last_ones = ones

                b = advance(b)

        answer = 0
        for total in totals_for_window.values():
            answer = max(answer, total)
        return answer
