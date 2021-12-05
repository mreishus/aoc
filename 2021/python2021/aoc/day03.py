#!/usr/bin/env python
"""
Advent Of Code 2021 Day 03
https://adventofcode.com/2021/day/3
"""
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        return [(line.strip()) for line in file.readlines()]


def bit_criteria_selection(data, most_common=True):
    candidates = set(range(len(data)))

    target = None
    for i, _ in enumerate(data[0]):
        seen = defaultdict(int)
        for cand in candidates:
            seen[data[cand][i]] += 1

        if seen["0"] > seen["1"]:
            target = "0" if most_common else "1"
        else:
            target = "1" if most_common else "0"

        to_remove = [cand for cand in candidates if data[cand][i] != target]
        candidates -= set(to_remove)
        if len(candidates) == 1:
            return int(data[list(candidates)[0]], 2)
    raise ValueError


class Day03:
    """ AoC 2021 Day 03 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 03 part 1 """
        data = parse(filename)

        common = ""
        leastc = ""
        for i, _ in enumerate(data[0]):
            seen = defaultdict(int)
            for item in data:
                seen[item[i]] += 1

            if seen["0"] > seen["1"]:
                common += "0"
                leastc += "1"
            else:
                common += "1"
                leastc += "0"
        gamma = int(common, 2)
        epi = int(leastc, 2)
        return gamma * epi

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 03 part 2 """
        data = parse(filename)

        o2 = bit_criteria_selection(data, True)
        co2 = bit_criteria_selection(data, False)

        return co2 * o2
