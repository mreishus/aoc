#!/usr/bin/env python
"""
Advent Of Code 2015 Day 3
https://adventofcode.com/2015/day/3
"""

from collections import defaultdict


def parse(filename: str):
    """ Given a filename, returns the first line of a file. """
    with open(filename) as file:
        return file.readline().strip()


def count_visited(directions: str, num_santas: int):
    deltas = {
        ">": complex(1, 0),
        "<": complex(-1, 0),
        "^": complex(0, 1),
        "v": complex(0, -1),
    }
    locs = [complex(0, 0)] * num_santas
    seen = defaultdict(int)
    seen[locs[0]] += 1
    i = 0

    for char in directions:
        locs[i] += deltas[char]
        seen[locs[i]] += 1
        i = (i + 1) % num_santas
    return len(seen.keys())


class Day03:
    """ AoC 2015 Day 03 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 03 part 1 """
        directions = parse(filename)
        return count_visited(directions, 1)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 21 part 2 """
        directions = parse(filename)
        return count_visited(directions, 2)
