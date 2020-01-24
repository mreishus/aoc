#!/usr/bin/env python
"""
Advent Of Code 2015 Day 4
https://adventofcode.com/2015/day/4
"""

from aoc.parsers import first_line
import hashlib


def is_pw(key: str, num: int, leading_zeros: int) -> bool:
    m = hashlib.md5()
    k = key + str(num)
    m.update(k.encode("utf-8"))
    target = "0" * leading_zeros
    return m.hexdigest()[0:leading_zeros] == target


def first_password(key: str, leading_zeros: int) -> int:
    for i in range(100_000_000):
        if is_pw(key, i, leading_zeros):
            return i
    return None


class Day04:
    """ AoC 2015 Day 04 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 04 part 1 """
        key = first_line(filename)
        return first_password(key, 5)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 21 part 2 """
        key = first_line(filename)
        return first_password(key, 6)
