#!/usr/bin/env python
"""
Advent Of Code 2024 Day 19
https://adventofcode.com/2024/day/19
"""
from typing import List
import re
from functools import lru_cache

class Hashabledict(dict):
    def __hash__(self):
        return hash(frozenset(self)) # only covers keys, trust needed

@lru_cache(maxsize=None)
def count_descendants(num, steps):
    if steps == 0:
        return 1

    if num == 0:
        return count_descendants(1, steps - 1)
    elif len(str(num)) % 2 == 0:
        s = str(num)
        mid = len(s)//2
        return (count_descendants(int(s[:mid]), steps - 1) +
                count_descendants(int(s[mid:]), steps - 1))
    else:
        return count_descendants(num * 2024, steps - 1)

@lru_cache(maxsize=None)
def is_possible(design, patterns):
    # des ('b', 'g', 'g', 'r')
    # pat {'r': [('r',), ('r', 'b')], 'w': [('w', 'r')], 'b': [('b',), ('b', 'w', 'u'), ('b', 'r')], 'g': [('g',),
    print("des", design)
    print("pat", patterns)
    if len(design) == 0:
        return True

    first_letter = design[0]
    if first_letter not in patterns:
        return False

    our_possible = False
    for cand in patterns[first_letter]:
        print("Considering", cand)
        lc = len(cand)
        print("  ", end="")
        print(design[0:lc])
        if (design[0:lc] == cand):
            this_possible = is_possible(design[lc:], patterns)
            if this_possible:
                our_possible = True
                break

    return our_possible

def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

def parse(filename):
    with open(filename) as file:
        string = file.read().strip()
    patterns_str, designs = string.split("\n\n")
    patterns = Hashabledict()
    for p in patterns_str.split(", "):
        the_pattern = tuple(p)
        first_letter = the_pattern[0]
        if first_letter in patterns:
            patterns[first_letter].append(the_pattern)
        else:
            patterns[first_letter] = [ the_pattern ]
    designs = designs.split("\n")
    return patterns, designs

class Day19:
    """AoC 2024 Day 19"""

    @staticmethod
    def part1(filename: str) -> int:
        patterns, designs = parse(filename)
        c = 0
        for design in designs:
            if is_possible(tuple(design), patterns):
                c += 1
        return c

    @staticmethod
    def part2(filename: str) -> int:
        return -1
