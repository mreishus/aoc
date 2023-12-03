#!/usr/bin/env python
"""
Advent Of Code 2023 Day 3
https://adventofcode.com/2023/day/3
"""
import re


class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.part_numbers = set()

    def parse(self, filename: str):
        self.max_x = 0
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[x, y] = char
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def compute_part_numbers(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                here = self.grid[x, y]
                if not here.isdigit() and here != ".":
                    for xx, yy in self.get_neighbors(x, y):
                        self.part_numbers.add((xx, yy))

    def part1(self):
        total = 0
        for y in range(self.max_y):
            x = 0
            this_digit = 0
            looking_at_digit = False
            digit_xs = []
            while x < self.max_x:
                here = self.grid[x, y]

                if here.isdigit():
                    looking_at_digit = True
                    digit_xs.append(x)
                    this_digit = (this_digit * 10) + int(here)
                    x += 1
                else:
                    if looking_at_digit:
                        print(f"Found digit {this_digit} at {digit_xs}, {y}")
                        ## Just finished a digit
                        for xx in digit_xs:
                            if (xx, y) in self.part_numbers:
                                print("  This is a part number")
                                total += this_digit
                                break
                        this_digit = 0
                        digit_xs = []
                    looking_at_digit = False
                    x += 1
            ## Before we go to the next line, check if we just finished a digit
            if looking_at_digit:
                print(f"Found digit {this_digit} at {digit_xs}, {y}")
                ## Just finished a digit
                for xx in digit_xs:
                    if (xx, y) in self.part_numbers:
                        print("  This is a part number")
                        total += this_digit
                        break

        return total

    def get_neighbors(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if (x + dx, y + dy) in self.grid:
                    yield (x + dx, y + dy)


class Day03:
    """AoC 2023 Day 03"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        g.compute_part_numbers()
        return g.part1()
        ## Incorrect answer 1: 524521
        ## I forgot to account for numbers that end at the end of the line

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return -1
