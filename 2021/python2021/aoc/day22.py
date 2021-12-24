#!/usr/bin/env python
"""
Advent Of Code 2021 Day 22
https://adventofcode.com/2021/day/22
"""
from typing import List
import re


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    on = line.startswith("on")
    [x1, x2, y1, y2, z1, z2] = ints(line)
    return [on, x1, x2, y1, y2, z1, z2]


class Range:
    def __init__(self, x1, x2, y1, y2, z1, z2, operation):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.operation = operation

    def is_overlap(self, other):
        x_over = False
        y_over = False
        z_over = False
        if self.x1 <= other.x1 and other.x1 <= self.x2:
            x_over = True
        if other.x1 <= self.x1 and self.x1 <= other.x2:
            x_over = True
        if not x_over:
            return False

        if self.y1 <= other.y1 and other.y1 <= self.y2:
            y_over = True
        if other.y1 <= self.y1 and self.y1 <= other.y2:
            y_over = True
        if not y_over:
            return False

        if self.z1 <= other.z1 and other.z1 <= self.z2:
            z_over = True
        if other.z1 <= self.z1 and self.z1 <= other.z2:
            z_over = True
        return x_over and y_over and z_over

    def clamp(self, other, operation=None):
        if not self.is_overlap(other):
            raise ValueError
        x1 = max(self.x1, other.x1)
        x2 = min(self.x2, other.x2)
        y1 = max(self.y1, other.y1)
        y2 = min(self.y2, other.y2)
        z1 = max(self.z1, other.z1)
        z2 = min(self.z2, other.z2)
        if operation is None:
            operation = self.operation
        return Range(x1, x2, y1, y2, z1, z2, operation)

    def area(self):
        x_size = self.x2 - self.x1 + 1
        y_size = self.y2 - self.y1 + 1
        z_size = self.z2 - self.z1 + 1
        return x_size * y_size * z_size

    def __repr__(self):
        return f"[{self.x1}..{self.x2}, {self.y1}..{self.y2}, {self.z1}..{self.z2}]={self.operation}"

    def __hash__(self):
        return hash(
            (self.x1, self.x2, self.y1, self.y2, self.z1, self.z2, self.operation)
        )

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (
            self.x1 == other.x1
            and self.x2 == other.x2
            and self.y1 == other.y1
            and self.y2 == other.y2
            and self.z1 == other.z1
            and self.z2 == other.z2
            and self.operation == other.operation
        )


def compute_ranges(ranges):
    processed = []
    for r in ranges:
        overlaps = []
        for p in processed:
            if r.is_overlap(p):
                # r subtract p postive -> negative
                # r subtract p subtract -> positive
                o = r.clamp(p, not p.operation)
                overlaps.append(o)
        processed += overlaps
        if r.operation:
            processed.append(r)
    area = 0
    for p in processed:
        sign = 1 if p.operation else -1
        area += p.area() * sign
    return area


class Day22:
    """ AoC 2021 Day 22 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 22 part 1 """
        data = parse(filename)
        look = Range(-50, 50, -50, 50, -50, 50, False)

        ## Build ranges and clamp to 50
        ranges = []
        for operation, x1, x2, y1, y2, z1, z2 in data:
            r = Range(x1, x2, y1, y2, z1, z2, operation)
            if look.is_overlap(r):
                ranges.append(r.clamp(look))
        return compute_ranges(ranges)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)

        ranges = []
        for operation, x1, x2, y1, y2, z1, z2 in data:
            r = Range(x1, x2, y1, y2, z1, z2, operation)
            ranges.append(r)
        return compute_ranges(ranges)
