#!/usr/bin/env python
"""
Advent Of Code 2015 Day 15
https://adventofcode.com/2015/day/15
"""

import re
from dataclasses import dataclass
from aoc.parsers import all_lines

PARSER = re.compile(
    r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
)


@dataclass
class Ingred:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse_line(line: str) -> Ingred:
    match = re.search(PARSER, line)
    if not match:
        raise ValueError("can't parse")
    (name, capacity, durability, flavor, texture, calories) = match.group(
        1, 2, 3, 4, 5, 6
    )
    return Ingred(
        name, int(capacity), int(durability), int(flavor), int(texture), int(calories)
    )


def part1(ings, target_cals):
    maxv = 100
    max_score_seen = 0
    for i in range(1, maxv + 1):
        for j in range(1, maxv + 1 - i):
            for k in range(1, maxv + 1 - i - j):
                l = maxv - i - j - k

                amounts = [i, j, k, l]
                cap = sum(amounts[a] * ings[a].capacity for a in [0, 1, 2, 3])
                dur = sum(amounts[a] * ings[a].durability for a in [0, 1, 2, 3])
                fla = sum(amounts[a] * ings[a].flavor for a in [0, 1, 2, 3])
                tex = sum(amounts[a] * ings[a].texture for a in [0, 1, 2, 3])

                cap = max(0, cap)
                dur = max(0, dur)
                fla = max(0, fla)
                tex = max(0, tex)

                if target_cals is not None:
                    cals = sum(amounts[a] * ings[a].calories for a in [0, 1, 2, 3])
                    if cals != target_cals:
                        continue

                this_score = cap * dur * fla * tex

                if this_score > max_score_seen:
                    max_score_seen = this_score

    return max_score_seen


class Day15:
    """ AoC 2015 Day 15 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 15 part 1 """
        ings = [parse_line(line) for line in all_lines(filename)]
        return part1(ings, None)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 15 part 2 """
        ings = [parse_line(line) for line in all_lines(filename)]
        return part1(ings, 500)
