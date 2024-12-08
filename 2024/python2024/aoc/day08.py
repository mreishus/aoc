#!/usr/bin/env python
"""
Advent Of Code 2024 Day 08
https://adventofcode.com/2024/day/7
"""
from typing import List
import re
from collections import deque, defaultdict
from math import sqrt

class Grid:
    def __init__(self):
        self.grid = {}
        self.grid = defaultdict(lambda: "Z", self.grid)
        self.max_x = 0
        self.max_y = 0
        self.ant_types = set()
        self.ant_map = defaultdict(list)
        self.ani_grid = defaultdict(list)
        self.all_anis = set()

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[(x, y)] = char
                    if char != '.':
                        self.ant_types.add(char)
                        self.ant_map[char].append( (x, y) )
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) in self.all_anis:
                    print("#", end="")
                else: 
                    print(self.grid[(x, y)], end="")
            print()

    def p1(self):
        self.add_anis()
        self.display()
        return len( self.all_anis )
        return 0

    def add_anis(self):
        for tipe in self.ant_types:
            print(tipe)
            locations = self.ant_map[tipe]
            for i in range(len(locations)):
                for j in range(i+1, len(locations)):
                    (n1x, n1y) = locations[i]
                    (n2x, n2y) = locations[j]

                    x_dist = n2x - n1x
                    y_dist = n2y - n1y
                    dist = sqrt( x_dist ** 2 + y_dist ** 2 )
                    slope = y_dist / x_dist

                    new_x_right = max(n1x, n2x) + abs(x_dist)
                    new_x_left  = min(n1x, n2x) - abs(x_dist)
                    if slope >= 0: # Remember, my "0" is on top, slope is "reversed"
                        pass
                        new_y_right = max(n1y, n2y) + abs(y_dist)
                        new_y_left  = min(n1y, n2y) - abs(y_dist)
                    else:
                        pass
                        new_y_right = min(n1y, n2y) - abs(y_dist)
                        new_y_left  = max(n1y, n2y) + abs(y_dist)

                    candidates = [
                        (new_x_right, new_y_right),
                        (new_x_left, new_y_left),
                    ]
                    for (new_x, new_y) in candidates:
                        if 0 <= new_x < self.max_x:
                            if 0 <= new_y < self.max_y:
                                self.all_anis.add( (new_x, new_y) )


class Day08:
    """AoC 2024 Day 08"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        # print(g.grid)
        # print(g.ant_types)
        # print(g.ant_map)
        return g.p1()

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        count = 0
        for (test_value, nums) in data:
            sol = dfs(nums, test_value, is_p2=True)
            if sol:
                count += test_value
        return count
