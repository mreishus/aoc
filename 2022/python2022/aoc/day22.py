#!/usr/bin/env python
"""
Advent Of Code 2022 Day 22
https://adventofcode.com/2022/day/22
"""
from typing import List
import re
from collections import defaultdict

PARSER = re.compile(r"(\d+)([L|R])?")


def parse(filename: str):
    """
    Parse the input file into a list of integers.
    Each integer is the sum of the numbers in a block.
    """
    with open(filename) as file:
        lines = file.read()
        maze, dirs = lines.split("\n\n")
        return parse_maze(maze), parse_dirs(dirs)


def parse_maze(maze):
    g = Grid()
    g.parse(maze)
    return g


def parse_dirs(dirs):
    r = []
    z = re.findall(PARSER, dirs)
    for (x, y) in z:
        r.append(int(x))
        if y:
            r.append(y)
    return r


class Grid:
    def __init__(self):
        self.grid = defaultdict(lambda: " ")
        self.max_x = 0
        self.max_y = 0
        self.init = None
        self.dir = (1, 0)
        #  RIGHT DOWN LEFT UP
        self.dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def parse(self, data):
        for y, line in enumerate(data.splitlines()):
            for x, char in enumerate(line.rstrip("\n")):
                if char != " ":
                    self.grid[x, y] = char
                    if self.init is None and y == 0:
                        print("Setting init to ", x, y)
                        self.init = (x, y)
                self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)

    def p1(self, instructions):
        print(self.grid)
        loc = self.init
        for inst in instructions:
            print(" ==> ", inst)
            if inst == "L":
                self.turn_left()
            elif inst == "R":
                self.turn_right()
            else:
                for _ in range(inst):
                    loc = self.move(loc)
                    print(loc)

        (x, y) = loc
        xx = x + 1
        yy = y + 1

        print("Done:", xx, yy)
        print("Facing: ", self.dir)
        print("Facing index: ", self.dirs.index(self.dir))
        pw = 1000 * yy + 4 * xx + self.dirs.index(self.dir)
        print("Final password: ", pw)
        return pw

    def next_tile(self, loc):
        x, y = loc
        dx, dy = self.dir
        x += dx
        y += dy
        if self.grid[x, y] == " ":
            print("Trying to warp")
            ## Warp like pacman
            if self.dir == (1, 0):
                x = 0
                while self.grid[x, y] == " ":
                    x += 1
            elif self.dir == (-1, 0):
                x = self.max_x
                while self.grid[x, y] == " ":
                    x -= 1
            elif self.dir == (0, 1):
                y = 0
                while self.grid[x, y] == " ":
                    y += 1
            elif self.dir == (0, -1):
                y = self.max_y
                while self.grid[x, y] == " ":
                    y -= 1

        return x, y  # self.grid[x, y]

    def move(self, loc):
        x, y = loc
        xx, yy = self.next_tile(loc)
        if self.grid[xx, yy] == "#":
            print("Hit a wall")
            return loc
        if self.grid[xx, yy] == " ":
            print("Hit a warp- Should not happen")
            exit()
        return xx, yy

    def turn_right(self):
        i = self.dirs.index(self.dir)
        self.dir = self.get_dir(i + 1)

    def turn_left(self):
        i = self.dirs.index(self.dir)
        self.dir = self.get_dir(i - 1)

    def get_dir(self, i):
        return self.dirs[i % 4]


class Day22:
    """AoC 2022 Day 22"""

    @staticmethod
    def part1(filename: str) -> int:
        maze, dirs = parse(filename)
        return maze.p1(dirs)

    @staticmethod
    def part2(filename: str) -> int:
        maze, dirs = parse(filename)
        return maze.p1(dirs)
