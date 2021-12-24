#!/usr/bin/env python
"""
Advent Of Code 2021 Day 22
https://adventofcode.com/2021/day/22
"""
from typing import List
import re
import math
from copy import deepcopy


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
        # print(f"Isoverlap {self} {other}")
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

    def has_subset(self, other):
        x_subset = False
        y_subset = False
        z_subset = False
        if self.x1 <= other.x1 and other.x2 <= self.x2:
            x_subset = True
        if self.y1 <= other.y1 and other.y2 <= self.y2:
            y_subset = True
        if self.z1 <= other.z1 and other.z2 <= self.z2:
            z_subset = True
        return x_subset and y_subset and z_subset

    def has_inverse(self, other):
        return (
            self.x1 == other.x1
            and self.x2 == other.x2
            and self.y1 == other.y1
            and self.y2 == other.y2
            and self.z1 == other.z1
            and self.z2 == other.z2
            and self.operation != other.operation
        )

    def overlap_area(self, other):
        x_overlap = max(0, min(self.x2 + 1, other.x2 + 1) - max(self.x1, other.x1))
        y_overlap = max(0, min(self.y2 + 1, other.y2 + 1) - max(self.y1, other.y1))
        z_overlap = max(0, min(self.z2 + 1, other.z2 + 1) - max(self.z1, other.z1))
        return x_overlap * y_overlap * z_overlap

    def clamp(self, other):
        if not self.is_overlap(other):
            raise ValueError
        x1 = max(self.x1, other.x1)
        x2 = min(self.x2, other.x2)
        y1 = max(self.y1, other.y1)
        y2 = min(self.y2, other.y2)
        z1 = max(self.z1, other.z1)
        z2 = min(self.z2, other.z2)
        return Range(x1, x2, y1, y2, z1, z2, self.operation)

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


def compose(lefts, r):
    rights = [r]
    operation = r.operation

    lefts, rights = two_piece_split_x(lefts, rights, not operation)

    to_add = []
    to_remove = set()
    # print(f"checking against {lefts}")
    for right in rights:
        if operation:
            # CASE: ADD
            overlap = any(right.is_overlap(l) for l in lefts)
            if overlap:
                # Don't count twice
                pass
            else:
                to_add.append(right)
        else:
            # CASE: SUBTRACT
            overlap = any(right.is_overlap(l) for l in lefts)
            if overlap:
                # Need to remove this region (right) from the lefts
                ## Make a copy of the subtract region with operation set to ADD
                ## So we can find it in a == comparison when removing
                new = deepcopy(right)
                new.operation = True
                to_remove.add(new)

    print(lefts, to_add, to_remove)
    return [x for x in lefts + to_add if not x in to_remove]


def two_piece_split_x(ls, rs, is_sub):
    xs = []
    for l in ls:
        if any(l.is_overlap(r) for r in rs):
            xs.append(l.x1)
            xs.append(l.x2)
    for r in rs:
        if any(r.is_overlap(l) for l in ls):
            xs.append(r.x1)
            xs.append(r.x2)
    ls = split_x(ls, xs, is_sub)
    rs = split_x(rs, xs, is_sub)

    ys = []
    for l in ls:
        if any(l.is_overlap(r) for r in rs):
            ys.append(l.y1)
            ys.append(l.y2)
    for r in rs:
        if any(r.is_overlap(l) for l in ls):
            ys.append(r.y1)
            ys.append(r.y2)
    ls = split_y(ls, ys, is_sub)
    rs = split_y(rs, ys, is_sub)

    zs = []
    for l in ls:
        if any(l.is_overlap(r) for r in rs):
            zs.append(l.z1)
            zs.append(l.z2)
    for r in rs:
        if any(r.is_overlap(l) for l in ls):
            zs.append(r.z1)
            zs.append(r.z2)
    ls = split_z(ls, zs, is_sub)
    rs = split_z(rs, zs, is_sub)

    return ls, rs


def split_x(regions, xs, is_subtracting):
    xs = sorted(xs)
    for x in xs:
        new_regions = []
        for r in regions:
            if r.x1 < x and x < r.x2:
                new1 = deepcopy(r)
                new2 = deepcopy(r)
                if is_subtracting:
                    new1.x2 = x - 1
                    new2.x1 = x
                else:
                    new1.x2 = x
                    new2.x1 = x + 1
                new_regions.append(new1)
                new_regions.append(new2)
            else:
                new_regions.append(r)
        regions = new_regions
    return regions


def split_y(regions, ys, is_subtracting):
    ys = sorted(ys)
    for y in ys:
        new_regions = []
        for r in regions:
            if r.y1 < y and y < r.y2:
                new1 = deepcopy(r)
                new2 = deepcopy(r)
                if is_subtracting:
                    new1.y2 = y - 1
                    new2.y1 = y
                else:
                    new1.y2 = y
                    new2.y1 = y + 1
                new_regions.append(new1)
                new_regions.append(new2)
            else:
                new_regions.append(r)
        regions = new_regions
    return regions


def split_z(regions, zs, is_subtracting):
    zs = sorted(zs)
    for z in zs:
        new_regions = []
        for r in regions:
            if r.z1 < z and z < r.z2:
                new1 = deepcopy(r)
                new2 = deepcopy(r)
                if is_subtracting:
                    new1.z2 = z - 1
                    new2.z1 = z
                else:
                    new1.z2 = z
                    new2.z1 = z + 1
                new_regions.append(new1)
                new_regions.append(new2)
            else:
                new_regions.append(r)
        regions = new_regions
    return regions


def rangesum(regions):
    area = 0
    for r in regions:
        area += r.area()
    return area


class Day22:
    """ AoC 2021 Day 22 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 22 part 1 """
        print("")
        data = parse(filename)

        look = Range(-50, 50, -50, 50, -50, 50, False)

        ## Build ranges and clamp to 50
        ranges = []
        for operation, x1, x2, y1, y2, z1, z2 in data:
            r = Range(x1, x2, y1, y2, z1, z2, operation)
            if look.is_overlap(r):
                ranges.append(r)

        # print("total area dumb:")
        # print(rangesum(ranges))

        processed = [ranges.pop(0)]
        print(rangesum(processed))
        for r in ranges:
            processed = compose(processed, r)
            print(rangesum(processed))
        # print("Done processing:")
        # print(processed)
        print("total area smart:")
        print(rangesum(processed))

        return -1

    @staticmethod
    def part2(filename: str) -> int:
        return -1


if __name__ == "__main__":
    print("2021 Day 22 Part 1:", end=" ")
    print(Day22.part1("../inputs/22/input_small2.txt"))
