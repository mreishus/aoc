#!/usr/bin/env python
"""
Advent Of Code 2025 Day 5
https://adventofcode.com/2025/day/5
"""

def parse(filename: str):
    with open(filename) as file:
        top, bottom = file.read().strip().split("\n\n")
    tops = []
    bottoms = []
    for line in top.split("\n"):
        left, right = line.split("-")
        tops.append( (int(left), int(right)) )
    for line in bottom.split("\n"):
        bottoms.append(int(line))
    return tops, bottoms

def solve1(fresh, available):
    c = 0
    for id in available:
        for l, h in fresh:
            if l <= id <= h:
                c += 1
                break
    return c

def solve2(fresh):
    """
    YES:
        l---------h
    ll------hh

    YES:
    l---------h
        ll--------hh

    YES:
    l-----------------h
        ll-----hh

    YES:
        l-----h
    ll-----------------hh

    NO:
    l----h
                ll------hh

    NO:
                l----h
    ll----hh
    """

    deduped = []
    for l, h in fresh:
        to_delete = []
        for i, (ll, hh) in enumerate(deduped):
            if l <= hh and ll <= h:
                to_delete.append(i)
                l = min(l, ll)
                h = max(h, hh)
        to_delete = sorted(set(to_delete))
        for j in reversed(to_delete):
            del deduped[j]
        if (l, h) not in deduped:
            deduped.append((l, h))

    c = 0
    for l, h in deduped:
        c += (h - l) + 1
    return c

class Day05:
    """AoC 2025 Day 05"""

    @staticmethod
    def part1(filename: str) -> int:
        fresh, available = parse(filename)
        return solve1(fresh, available)

    @staticmethod
    def part2(filename: str) -> int:
        fresh, _ = parse(filename)
        return solve2(fresh)

