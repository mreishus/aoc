#!/usr/bin/env python
"""
Advent Of Code 2024 Day 16
https://adventofcode.com/2024/day/16
"""
from typing import List
import re
from aoc.heapdict import heapdict
from collections import defaultdict
# from z3 import Optimize, sat, Ints, Or

class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.start = (-1, -1)
        self.end = (-1, -1)
        self.dir = (1, 0)

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    if char == 'S':
                        self.start = (x, y)
                        self.grid[(x, y)] = '.'
                    elif char == 'E':
                        self.end = (x, y)
                        self.grid[(x, y)] = '.'
                    else:
                        self.grid[(x, y)] = char
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                print(self.grid[(x, y)], end="")
            print()
            self.max_y = max(self.max_y, y)

    def rotate_cc(self, dir):
        """Rotate direction counterclockwise
        (1,0)  -> (0,-1) -> (-1,0) -> (0,1)
        east   -> north  -> west   -> south
        """
        x, y = dir
        return (y, -x)

    def rotate_cw(self, dir):
        """Rotate direction clockwise
        (1,0)  -> (0,1)  -> (-1,0) -> (0,-1)
        east   -> south  -> west   -> north
        """
        x, y = dir
        return (-y, x)

    def next_states(self, state):
        (loc, dir) = state
        r1 = ((loc, self.rotate_cc(dir)), 1000, 'cc')
        r2 = ((loc, self.rotate_cw(dir)), 1000, 'cw')
        returns = [
            r1,
            r2
        ]
        (loc_x, loc_y) = loc
        (dir_x, dir_y) = dir
        new_loc = (loc_x + dir_x, loc_y + dir_y)
        if new_loc in self.grid and self.grid[new_loc] != '#':
            r3 = ((new_loc, dir), 1, 'forward')
            returns.append(r3)
        return returns

    def solve(self):
        init_state = (self.start, self.dir)
        dist_to = defaultdict(lambda: 999_999)
        edge_to = {}
        open_set = heapdict()

        dist_to[init_state] = 0
        open_set[init_state] = 0
        while len(open_set) > 0:
            (state, length) = open_set.popitem()
            (loc, _dir) = state

            if loc == self.end:
                return length

            for (new_state, cost, name) in self.next_states(state):
                if dist_to[new_state] > dist_to[state] + cost:
                    dist_to[new_state] = dist_to[state] + cost
                    edge_to[new_state] = (state, name)
                    open_set[new_state] = dist_to[new_state]

        return 0


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

class Day16:
    """AoC 2024 Day 16"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        g.display()
        return g.solve()

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        total = -1
        return total
