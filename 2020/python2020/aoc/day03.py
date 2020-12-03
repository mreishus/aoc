#!/usr/bin/env python
"""
Advent Of Code 2020 Day 3
https://adventofcode.com/2020/day/3
"""


class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0

    def parse(self, filename: str):
        loc = complex(0, 0)
        self.max_x = 0
        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[loc] = char
                    loc += complex(1, 0)
                    self.max_x = max(self.max_x, int(loc.real))
                loc += complex(0, 1)
                loc = complex(0, loc.imag)
                self.max_y = max(self.max_y, int(loc.imag))

    def at(self, x, y):
        if y >= self.max_y:
            return ""
        return self.grid[complex(x % self.max_x, y)]

    def atc(self, coord):
        x, y = int(coord.real), int(coord.imag)
        return self.at(x, y)

    def solve_p1(self):
        slope = complex(3, 1)
        return self.solve_slope(slope)

    def solve_p2(self):
        slopes = [
            complex(1, 1),
            complex(3, 1),
            complex(5, 1),
            complex(7, 1),
            complex(1, 2),
        ]
        answer = 1
        for slope in slopes:
            answer *= self.solve_slope(slope)
        return answer

    def solve_slope(self, slope):
        me = complex(0, 0)
        trees = 0
        while int(me.imag) <= self.max_y:
            me += slope
            if self.atc(me) == "#":
                trees += 1
        return trees


class Day03:
    """ AoC 2020 Day 03 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 03 part 1 """
        g = Grid()
        g.parse(filename)
        return g.solve_p1()

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 03 part 2 """
        g = Grid()
        g.parse(filename)
        return g.solve_p2()
