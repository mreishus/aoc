#!/usr/bin/env python
"""
Advent Of Code 2024 Day 21
https://adventofcode.com/2024/day/21
"""

from functools import lru_cache

numpad = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "x": (0, 3),  ## Cannot go here
    "0": (1, 3),
    "A": (2, 3),
}
inv_numpad = {v: k for k, v in numpad.items()}

arrowpad = {
    "x": (0, 0),  ## Cannot go here
    "^": (1, 0),
    "B": (2, 0),  ## Like A, but a diff character
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}
inv_arrowpad = {v: k for k, v in arrowpad.items()}


def steps_for(start_char, end_char):
    # Are we on the numpad or arrowpad?
    pad = arrowpad
    inv_pad = inv_arrowpad
    if start_char in numpad:
        pad = numpad
        inv_pad = inv_numpad

    (x1, y1) = pad[start_char]
    (x2, y2) = pad[end_char]
    dx = x2 - x1
    dy = y2 - y1

    x_steps = ""
    y_steps = ""
    if dx >= 0:
        x_steps = ">" * abs(dx)
    else:
        x_steps = "<" * abs(dx)
    if dy >= 0:
        y_steps = "v" * abs(dy)
    else:
        y_steps = "^" * abs(dy)

    # We can do all x steps, then all y steps, or the reverse.
    # However, one of them might bring us across the forbidden square: Check for that
    if inv_pad[(x2, y1)] == "x":
        # Cannot move horizontal first - would hit forbidden square "x"
        return [y_steps + x_steps + "B"]
    elif inv_pad[(x1, y2)] == "x":
        # Cannot move vertical first - would hit forbidden square "x"
        return [x_steps + y_steps + "B"]
    elif dx == 0:
        # Only vertical
        return [y_steps + "B"]
    elif dy == 0:
        # Only horizontal
        return [x_steps + "B"]
    else:
        return [x_steps + y_steps + "B", y_steps + x_steps + "B"]


@lru_cache(maxsize=None)
def min_count_for(previous_char, char, depth):
    steps2 = steps_for(previous_char, char)
    counts = []
    for s in steps2:
        counts.append(search_new(s, depth))
    return min(counts)


def search_new(code, depth):
    if depth == 0:
        return len(code)
    total = 0
    for i, char in enumerate(code):
        previous_char = code[i - 1]
        total += min_count_for(previous_char, char, depth - 1)
    return total


def parse(filename):
    with open(filename) as file:
        string = file.read().strip()
    return string.split("\n")


class Day21:
    """AoC 2024 Day 21"""

    @staticmethod
    def part1or2(filename: str, n: int) -> int:
        codes = parse(filename)
        total = 0
        for code in codes:
            ln = search_new(code, n + 1)
            numeric = int(code[:3])
            total += numeric * ln
        return total

    @staticmethod
    def part1(filename: str) -> int:
        return Day21.part1or2(filename, 2)

    @staticmethod
    def part2(filename: str) -> int:
        return Day21.part1or2(filename, 25)
