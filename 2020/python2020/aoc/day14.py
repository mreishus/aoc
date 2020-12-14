#!/usr/bin/env python
"""
Advent Of Code 2020 Day 14
https://adventofcode.com/2020/day/14
"""

import re
from collections import defaultdict
from itertools import combinations


def parse(filename):
    with open(filename) as f:
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


class Mask2:
    def __init__(self):
        self.do_clear_mask()

    def do_clear_mask(self):
        self.fill_mask = 0  # usually 0s, contains 1 to overwrite with 1
        self.unstables = []

    def update_from_string(self, mask_str):
        self.do_clear_mask()

        fill_add = 0
        for char in mask_str:
            fill_add *= 2
            if char == "1":
                fill_add += 1
        self.fill_mask |= fill_add

        for i, char in enumerate(mask_str):
            if char == "X":
                self.unstables.append(35 - i)
        # print(self.unstables)

    def apply_over_value(self, val_in):
        val = val_in | self.fill_mask
        for n in range(0, len(self.unstables) + 1):
            combos = combinations(self.unstables, n)

            # print("--")
            # print(n, combos)
            for this_combo in combos:
                unstable_fills = 0  # All 0s, contains 1 to overwrite with |
                unstable_clears = (2 ** 37) - 1
                # ^ Usually 1s, contains 0 to overwrite with &
                for this_unstable in self.unstables:
                    # print(f" {this_unstable} {this_unstable in this_combo}")
                    if this_unstable in this_combo:
                        # Flip ON
                        unstable_fills |= 2 ** this_unstable
                    else:
                        # Flip OFF
                        all_ones = 2 ** 37 - 1
                        clear_add = all_ones ^ (2 ** this_unstable)
                        unstable_clears &= clear_add
                yield (val | unstable_fills) & unstable_clears
            # print("Done")


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
    return sum(mem.values())


def p2(data):
    m = Mask2()
    mem = defaultdict(int)
    for (left, right) in data:
        if left == "mask":
            m.update_from_string(right)
        else:
            for z in m.apply_over_value(left):
                mem[z] = right
    return sum(mem.values())


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
        # m = Mask2()
        # m.update_from_string("000000000000000000000000000000X1001X")
        # for z in m.apply_over_value(42):
        #     print(z)
        # print("----")
        # m.update_from_string("00000000000000000000000000000000X0XX")
        # for z in m.apply_over_value(26):
        #     print(z)
        # return -1
        # data = parse(filename)
        # return p2(data)
