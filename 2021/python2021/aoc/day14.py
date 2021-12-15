#!/usr/bin/env python
"""
Advent Of Code 2021 Day 14
https://adventofcode.com/2021/day/8
"""
from typing import Tuple, Dict
from collections import defaultdict


def parse(filename: str) -> Tuple[str, Dict[str, str]]:
    with open(filename) as file:
        polymer, rules_lines = file.read().strip().split("\n\n")
        rules = {}
        for line in rules_lines.split("\n"):
            (left, right) = line.split(" -> ")
            rules[left] = right
        return polymer, rules


def score(pairs, first_char, last_char):
    seen = defaultdict(int)
    for pair, count in pairs.items():
        seen[pair[0]] += count
        seen[pair[1]] += count

    seen[first_char] += 1
    seen[last_char] += 1
    for char in seen.keys():
        seen[char] //= 2

    return max(seen.values()) - min(seen.values())


def string_to_pairs(polymer_str: str):
    pairs = defaultdict(int)
    for (x1, x2) in zip(polymer_str, polymer_str[1:]):
        pairs[x1 + x2] += 1
    return pairs


def expand(pairs, rules):
    delta = defaultdict(int)
    for pair, count in pairs.items():
        if pair not in rules or count == 0:
            continue
        middle = rules[pair]

        delta[pair[0] + middle] += count
        delta[middle + pair[1]] += count
        delta[pair] -= count

    for pair, count in delta.items():
        pairs[pair] += count

    return pairs


class Day14:
    """ AoC 2021 Day 14 """

    @staticmethod
    def partX(filename: str, steps: int) -> int:
        polymer_str, rules = parse(filename)
        first_char = polymer_str[0]
        last_char = polymer_str[-1]
        pairs = string_to_pairs(polymer_str)
        for i in range(steps):
            pairs = expand(pairs, rules)
        return score(pairs, first_char, last_char)

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 14 part 1 """
        return Day14.partX(filename, 10)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 14 part 2 """
        return Day14.partX(filename, 40)
