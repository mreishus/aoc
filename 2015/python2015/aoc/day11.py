#!/usr/bin/env python
"""
Advent Of Code 2015 Day 11
https://adventofcode.com/2015/day/11
"""

import re
from aoc.parsers import first_line

PAIR = re.compile(r"(.)\1")
FORBIDDEN = re.compile(r"[iol]")

def inc(password: str) -> str:
    """
    Increments a string.
    Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on.
    Increase the rightmost letter one step; if it was z, it wraps around to a, and
    repeat with the next letter to the left until one doesn't wrap around.
    """
    letters = [c for c in password]
    for i, char in reversed(list(enumerate(letters))):
        letters[i] = inc_char(char)
        if letters[i] != 'a':
            break
    return "".join(letters)

def is_valid(password: str) -> bool:
    return not has_forbidden_chars(password) and has_two_pairs(password) and has_run(password)

def has_forbidden_chars(password: str) -> bool:
    return bool(re.search(FORBIDDEN, password))

def has_two_pairs(password: str) -> bool:
    matches = re.findall(PAIR, password)
    return len(set(matches)) > 1

def has_run(password: str) -> bool:
    for (c1, c2, c3) in zip(password, password[1:], password[2:]):
        if ord(c3) == ord(c2) + 1 and ord(c2) == ord(c1) + 1:
            return True
    return False

def inc_char(password: str) -> str:
    num = ord(password)
    if 97 <= num <= 122:
        num -= 97
        num += 1
        num = num % 26
        num += 97
    elif 65 <= num <= 90:
        num -= 65
        num += 1
        num = num % 26
        num += 65
    else:
        raise ValueError("Don't know how to inc_char this")
    return chr(num)

def next_pw(password: str) -> str:
    while True:
        password = inc(password)
        if is_valid(password):
            return password

class Day11:
    """ AoC 2015 Day 11 """

    @staticmethod
    def part1(filename: str) -> str:
        """ Given a filename, solve 2015 day 11 part 1 """
        password = first_line(filename)
        return next_pw(password)

    @staticmethod
    def part2(filename: str) -> str:
        """ Given a filename, solve 2015 day 11 part 2 """
        password = first_line(filename)
        return next_pw(next_pw(password))
