#!/usr/bin/env python
"""
Advent Of Code 2015 Day 8
https://adventofcode.com/2015/day/8
"""

import re
from aoc.parsers import all_lines


ESCAPE_DOUBLE = re.compile(r"\\\"")
ESCAPE_BACKSLASH = re.compile(r"\\\\")
ESCAPE_HEX = re.compile(r"\\x[0-9a-fA-F][0-9a-fA-F]")
BACKSLASH = re.compile(r"\\")
QUOTE = re.compile(r"\"")

def len_code(orig_string: str) -> int:
    if orig_string[0] != '"' or orig_string[-1] != '"':
        raise ValueError("len_code: expected a double quoted string")

    string = orig_string[1:-1]
    num_escape_double = len(re.findall(ESCAPE_DOUBLE, string))
    num_escape_backslash = len(re.findall(ESCAPE_BACKSLASH, string))
    num_escape_hex = len(re.findall(ESCAPE_HEX, string))
    extra_chars = 2 + num_escape_double + num_escape_backslash + (num_escape_hex * 3)
    return len(orig_string) - extra_chars

def len_expand(orig_string: str) -> int:
    if orig_string[0] != '"' or orig_string[-1] != '"':
        raise ValueError("len_code: expected a double quoted string")

    string = orig_string[1:-1]
    num_backslash = len(re.findall(BACKSLASH, string))
    num_quote = len(re.findall(QUOTE, string))
    return len(orig_string) + 4 + num_backslash + num_quote

class Day08:
    """ AoC 2015 Day 08 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 08 part 1 """
        lines = all_lines(filename)
        real_lens = sum(len(line) for line in lines)
        code_lens = sum(len_code(line) for line in lines)
        return real_lens - code_lens

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 08 part 2 """
        lines = all_lines(filename)
        real_lens = sum(len(line) for line in lines)
        expand_lens = sum(len_expand(line) for line in lines)
        return expand_lens - real_lens
