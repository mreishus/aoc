#!/usr/bin/env python
"""
Advent Of Code 2022 Day 05
https://adventofcode.com/2022/day/5
"""
import re
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        lines = file.read()
        block1, block2 = lines.split("\n\n")
        return parse_stack(block1), parse_directions(block2)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def parse_stack(lines):
    stacks = defaultdict(list)
    for line in lines.splitlines():
        i = 0
        for chunk in chunks(line, 4):
            chunk = re.sub(r"\W", "", chunk)
            if len(chunk) > 0 and not chunk.isdigit():
                stacks[i].append(chunk)
            i += 1
    for i in range(len(stacks)):
        stacks[i].reverse()
    return stacks


def parse_directions(lines) -> list[list[int]]:
    return [ints(line) for line in lines.splitlines()]


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def process(stacks, direction):
    [num, frm, to] = direction
    frm -= 1
    to -= 1
    for _ in range(num):
        stacks[to].append(stacks[frm].pop())
    return stacks


def process2(stacks, direction):
    [num, frm, to] = direction
    frm -= 1
    to -= 1
    buffer = []
    for _ in range(num):
        buffer.append(stacks[frm].pop())
    for block in reversed(buffer):
        stacks[to].append(block)
    return stacks


class Day05:
    """AoC 2022 Day 05"""

    @staticmethod
    def part1(filename: str):
        stacks, directions = parse(filename)
        for direction in directions:
            stacks = process(stacks, direction)

        output = ""
        for i in range(len(stacks)):
            output += stacks[i].pop()
        return output

    @staticmethod
    def part2(filename: str):
        stacks, directions = parse(filename)
        for direction in directions:
            stacks = process2(stacks, direction)

        output = ""
        for i in range(len(stacks)):
            output += stacks[i].pop()
        return output
