#!/usr/bin/env python
"""
Advent Of Code 2024 Day 19
https://adventofcode.com/2024/day/19
"""
from functools import lru_cache

class Hashabledict(dict):
    def __hash__(self):
        return hash(frozenset(self)) # only covers keys, trust needed

@lru_cache(maxsize=None)
def is_possible(design, patterns):
    # des ('b', 'g', 'g', 'r')
    # pat {'r': [('r',), ('r', 'b')], 'w': [('w', 'r')], 'b': [('b',), ('b', 'w', 'u'), ('b', 'r')], 'g': [('g',),
    if len(design) == 0:
        return True

    first_letter = design[0]
    if first_letter not in patterns:
        return False

    our_possible = False
    for cand in patterns[first_letter]:
        lc = len(cand)
        if (design[0:lc] == cand):
            this_possible = is_possible(design[lc:], patterns)
            if this_possible:
                our_possible = True
                break

    return our_possible

@lru_cache(maxsize=None)
def is_possible2(design, patterns):
    # des ('b', 'g', 'g', 'r')
    # pat {'r': [('r',), ('r', 'b')], 'w': [('w', 'r')], 'b': [('b',), ('b', 'w', 'u'), ('b', 'r')], 'g': [('g',),
    if len(design) == 0:
        return 1

    first_letter = design[0]
    if first_letter not in patterns:
        return 0

    our_possible = 0
    for cand in patterns[first_letter]:
        lc = len(cand)
        if (design[0:lc] == cand):
            our_possible += is_possible2(design[lc:], patterns)

    return our_possible

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
        patterns, designs = parse(filename)
        c = 0
        for design in designs:
            c += is_possible2(tuple(design), patterns)
        return c
