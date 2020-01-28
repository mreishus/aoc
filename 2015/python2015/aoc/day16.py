#!/usr/bin/env python
"""
Advent Of Code 2016 Day 16
https://adventofcode.com/2016/day/16
"""

import re
import operator
from typing import Dict, List, Union
from aoc.parsers import all_lines

SUE_NUM_P = re.compile(r"Sue (\d+):")
THING_P = re.compile(r"(\w+): (\d+)")

TARGET = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

# Line example
# "Sue 22: vizslas: 6, trees: 8, akitas: 10"
# Output example
# { "num": 22, "vizslas": 6, "trees": 8, "akitas": 10 }
def parse_line(line: str) -> Dict[str, int]:
    match = re.search(SUE_NUM_P, line)
    num = int(match.group(1))
    sue = {"num": num}
    for (thing, amount) in re.findall(THING_P, line):
        sue[thing] = int(amount)
    return sue


def part1(sues: List[Dict[str, int]]) -> Union[int, None]:
    for sue in sues:
        possible_match = True
        for key in TARGET:
            if key in sue and sue[key] != TARGET[key]:
                possible_match = False
                break
        if possible_match:
            return sue["num"]
    return None


def part2(sues: List[Dict[str, int]]) -> Union[int, None]:
    # Cats/Trees: Match has greater than
    # Pomeranians/Goldfish: Match has fewer than
    # Disqualifying operators
    operators = {
        "cats": operator.le,
        "trees": operator.le,
        "pomeranians": operator.ge,
        "goldfish": operator.ge,
        "children": operator.ne,
        "samoyeds": operator.ne,
        "akitas": operator.ne,
        "vizslas": operator.ne,
        "cars": operator.ne,
        "perfumes": operator.ne,
    }
    for sue in sues:
        possible_match = True
        for key in TARGET:
            op = operators[key]
            if key in sue and op(sue[key], TARGET[key]):
                possible_match = False
                break
        if possible_match:
            return sue["num"]
    return None


class Day16:
    """ AoC 2016 Day 16 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2016 day 16 part 1 """
        sues = [parse_line(line) for line in all_lines(filename)]
        return part1(sues)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2016 day 16 part 2 """
        sues = [parse_line(line) for line in all_lines(filename)]
        return part2(sues)
