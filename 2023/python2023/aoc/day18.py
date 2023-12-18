#!/usr/bin/env python
"""
Advent Of Code 2023 Day 18
https://adventofcode.com/2023/day/18
"""
import re
from typing import List
from collections import defaultdict


class Grid:
    def __init__(self):
        self.grid = defaultdict(int)
        self.grid_colors = {}
        self.max_x = 0
        self.max_y = 0
        self.digger_loc = (50, 320)
        self.inside_point = None

    def execute_dig_plan(self, data):
        self.grid[self.digger_loc] = 1
        for line in data:
            # print(line)
            dx, dy = self.get_direction(line[0])
            distance = int(line[1])
            for i in range(distance):
                self.digger_loc = (self.digger_loc[0] + dx, self.digger_loc[1] + dy)
                self.grid[self.digger_loc] = 1

                if self.inside_point is None:
                    if line[0] == "R":
                        self.inside_point = (self.digger_loc[0], self.digger_loc[1] + 1)
                    elif line[0] == "L":
                        self.inside_point = (self.digger_loc[0], self.digger_loc[1] + 1)
                    elif line[0] == "D":
                        self.inside_point = (self.digger_loc[0] + 1, self.digger_loc[1])
                    elif line[0] == "U":
                        raise ValueError(
                            "Should not be here - Didn't expect U on first move"
                        )
                    else:
                        raise ValueError(f"Unknown direction: {line[0]}")

                # print("Digger loc:", self.digger_loc)
                ## Let's set max_x and max_y
                if self.digger_loc[0] > self.max_x:
                    self.max_x = self.digger_loc[0]
                if self.digger_loc[1] > self.max_y:
                    self.max_y = self.digger_loc[1]
            # self.display()

    def dig_out_interior(self):
        q = [self.inside_point]
        seen = set()
        while len(q) > 0:
            loc = q.pop(0)
            if loc in seen:
                continue
            seen.add(loc)

            ## Dig out the interior
            if loc not in self.grid or self.grid[loc] == 0:
                self.grid[loc] = 1

            ## Add neighbors to the queue
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x = loc[0] + dx
                y = loc[1] + dy
                if x < 0 or y < 0 or x > self.max_x or y > self.max_y:
                    continue
                if (x, y) in self.grid and self.grid[(x, y)] == 1:
                    continue
                q.append((x, y))

    def display(self):
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                if (x, y) in self.grid:
                    print("#", end="")
                elif (x, y) == self.inside_point:
                    print("X", end="")
                else:
                    print(".", end="")
            print()

    def get_direction(self, direction):
        ## Close, but R D L U
        if direction == "R":
            return 1, 0
        elif direction == "L":
            return -1, 0
        elif direction == "D":
            return 0, 1
        elif direction == "U":
            return 0, -1
        else:
            raise ValueError(f"Unknown direction: {direction}")

    def count_dug_space(self):
        ## Add up all values of grid
        return sum(self.grid.values())


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    ## R 6 (#70c710)
    matches = re.match(r"^(\w+)\s+(\d+)\s+(\(\#\w+\))$", line)
    if matches:
        return matches.groups()
    return line


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


class Day18:
    """AoC 2023 Day 18"""

    @staticmethod
    def part1(filename: str) -> int:
        print("")
        data = parse(filename)
        g = Grid()
        g.execute_dig_plan(data)
        # g.display()
        if len(data) > 100:
            g.inside_point = (g.inside_point[0] + 2, g.inside_point[1])
        g.dig_out_interior()
        g.display()
        return g.count_dug_space()
        ## Incorrect guess: 3153

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        print(data)
        return -1
