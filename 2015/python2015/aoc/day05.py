#!/usr/bin/env python
"""
Advent Of Code 2015 Day 5
https://adventofcode.com/2015/day/5
"""

import re
from aoc.parsers import all_lines

VOWELS = {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}
DOUBLE = re.compile(r"(.)\1")
DOUBLE_PAIR = re.compile(r"(..).*\1")
ABA = re.compile(r"(.).\1")
FORBIDDEN = re.compile(r"(ab|cd|pq|xy)")


def is_nice1(x: str) -> bool:
    """
    A nice string is one with all of the following properties:
        It contains at least three vowels (aeiou only), like aei, xazegov, or
        aeiouaeiouaeiou.
        It contains at least one letter that appears twice in a row, like xx,
        abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
        It does not contain the strings ab, cd, pq, or xy, even if they are
        part of one of the other requirements.
    """

    return three_or_more_vowels(x) and has_double(x) and not has_forbidden(x)


def three_or_more_vowels(string: str) -> bool:
    """ Does the string have at least three vowels (lowercase)? """
    count = 0
    for char in string:
        if char in VOWELS:
            count += 1
        if count >= 3:
            return True
    return False


def has_double(x: str) -> bool:
    """ Does the string contain a letter that appears twice in a row? """
    return bool(re.search(DOUBLE, x))


def has_forbidden(x: str) -> bool:
    """ Does the string contain one of the forbidden substrings "ab" "cd" "pq"
    "xy"? """
    return bool(re.search(FORBIDDEN, x))


def is_nice2(x: str) -> bool:
    """
    It contains a pair of any two letters that appears at least twice in the
    string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like
    aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter
    between them, like xyx, abcdefeghi (efe), or even aaa.
    """
    return bool(re.search(ABA, x)) and bool(re.search(DOUBLE_PAIR, x))


class Day05:
    """ AoC 2015 Day 05 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 05 part 1 """
        lines = all_lines(filename)
        return sum(1 for line in lines if is_nice1(line))

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 05 part 2 """
        lines = all_lines(filename)
        return sum(1 for line in lines if is_nice2(line))
