#!/usr/bin/env python
"""
Advent Of Code 2020 Day 2
https://adventofcode.com/2020/day/2
"""
from typing import List, Optional, Tuple
import re


class Policy:
    def __init__(self, lower, upper, letter):
        self.lower = lower
        self.upper = upper
        self.letter = letter

    def __repr__(self):
        return f"<Policy {self.lower}, {self.upper}, {self.letter}>"

    def test1(self, password):
        return self.lower <= password.count(self.letter) <= self.upper

    def test2(self, password):
        cand_lower = password[self.lower - 1]
        cand_upper = password[self.upper - 1]
        return (cand_lower == self.letter) ^ (cand_upper == self.letter)


def parse(filename: str) -> List[Tuple[Policy, str]]:
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    left, password = line.split(": ")
    lower, upper, letter = re.search(r"(\d+)-(\d+) (\w)", left).groups()
    lower = int(lower)
    upper = int(upper)
    pol = Policy(lower, upper, letter)
    return (pol, password)


class Day02:
    """ AoC 2020 Day 02 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 02 part 1 """
        data = parse(filename)
        valid_pw_count = sum(1 for (pol, password) in data if pol.test1(password))
        return valid_pw_count

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 02 part 2 """
        data = parse(filename)
        valid_pw_count = sum(1 for (pol, password) in data if pol.test2(password))
        return valid_pw_count
