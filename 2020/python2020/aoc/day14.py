#!/usr/bin/env python
"""
Advent Of Code 2020 Day 14
https://adventofcode.com/2020/day/14
"""

import re
from collections import defaultdict


def parse(filename):
    with open(filename) as f:
        # programs = []
        # program = None
        program = []
        for line in f.readlines():
            if re.match(r"mask = ", line):
                (mask) = re.match(r"mask = ([01X]+)$", line).groups()
                program.append(("mask", mask[0]))
            else:
                (left, right) = re.match(r"mem\[(\d+)\] = (\d+)$", line).groups()
                program.append((int(left), int(right)))
        return program


class Mask:
    def __init__(self):
        self.do_clear_mask()

    def do_clear_mask(self):
        self.fill_mask = 0  # Usually 0s, contains 1 to overwrite with |
        self.clear_mask = (2 ** 37) - 1  # Usually 1s, contains 0 to overwrite with &

    def update_from_string(self, mask_str):
        self.do_clear_mask()
        # print(f"BEFORE Fill mask : {self.fill_mask:037b}")
        # print(f"BEFORE Clear mask: {self.clear_mask:037b}")
        # Look for 1s to add to fill_mask
        fill_add = 0
        for char in mask_str:
            fill_add *= 2
            if char == "1":
                fill_add += 1
        # Apply
        # print(f"fill add: {fill_add}")
        self.fill_mask |= fill_add
        self.clear_mask |= fill_add
        # ^ Anything we found in fill_add, if it was previously set in
        # clear_mask, we have to clear it.

        # Look for 0s to add to clear_mask
        clear_add = 0
        for char in mask_str:
            clear_add *= 2
            if char == "0":
                clear_add += 1
        # Clear_add has 1s in spots we want to clear.  Flip to have
        # all 1s, but 0s in the space we want to clear
        all_ones = 2 ** 37 - 1
        clear_add = all_ones ^ clear_add
        ## Now use & to wipe out the clear mask
        self.clear_mask &= clear_add
        self.fill_mask &= clear_add
        # print(f"AFTER Fill mask : {self.fill_mask:037b}")
        # print(f"AFTER Clear mask: {self.clear_mask:037b}")

    def apply_over_value(self, val_in):
        return (val_in | self.fill_mask) & self.clear_mask


def parse_line(line):
    (left, right) = line[0:1], line[1:]
    right = int(right)
    return (left, right)


def p1(data):
    m = Mask()
    mem = defaultdict(int)
    for (left, right) in data:
        if left == "mask":
            m.update_from_string(right)
        else:
            mem[left] = m.apply_over_value(right)
    # (You guessed 520626422042.)
    # (You guessed 18925954113791.)
    # 18925954113791
    # 18925954113791
    return sum(mem.values())


def p2(data):
    return -2


class Day14:
    """ AoC 2020 Day 14 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 14 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 14 part 2 """
        data = parse(filename)
        return p2(data)
