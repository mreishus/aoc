#!/usr/bin/env python
"""
Advent Of Code 2024 Day 15
https://adventofcode.com/2024/day/15
"""
from typing import List
import re
from functools import lru_cache

class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.robot = (-1, -1)
        self.is_scaled = False

    def parse_str(self, str):
        x = 0
        y = 0

        for line in str.split("\n"):
            for char in line.strip():
                self.grid[(x, y)] = char
                if (char == '@'):
                    self.robot = (x, y)
                    self.grid[(x, y)] = '.'
                x += 1
                self.max_x = max(self.max_x, x)
            y += 1
            self.max_y = max(self.max_y, y)
            x = 0

    def gps(self):
        score = 0
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.grid[(x, y)] == 'O':
                    score += 100 * y + x
        return score

    def gps2(self):
        score = 0
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.grid[(x, y)] == '[':
                    score += 100 * y + x
        return score

    def move_robot(self, chardir):
        lookup = {
            '^': (0, -1),
            'v': (0, 1),
            '<': (-1, 0),
            '>': (1, 0),
        }
        if chardir not in lookup:
            # print("cd=", chardir)
            return
        dir = lookup[chardir]

        destination = tuple_add(self.robot, dir)
        #print(f"{self.robot} | {dir} | {destination}")
        if self.grid[destination] == 'O':
            # Found a rock in destination. Need to make sure
            # it's an optional string of rocks and then a empty space
            num_bots = 1
            dest2 = destination
            while True:
                dest2 = tuple_add(dest2, dir)
                if self.grid[dest2] != 'O':
                    break
                num_bots += 1

            if self.grid[dest2] == '#':
                # Cannot push. Do nothing.
                pass
            elif self.grid[dest2] == '.':
                # Push!
                self.grid[destination] = '.'
                self.grid[dest2] = 'O'
                self.robot = destination
            else:
                raise ValueError('wtf is dest2?')
        elif self.grid[destination] == '.':
            self.robot = destination
        elif self.grid[destination] == '#':
            pass
        else:
            raise ValueError("Something happened")

    def move_robot2(self, chardir):
        lookup = {
            '^': (0, -1),
            'v': (0, 1),
            '<': (-1, 0),
            '>': (1, 0),
        }
        if chardir not in lookup:
            # print("cd=", chardir)
            return
        dir = lookup[chardir]

        destination = tuple_add(self.robot, dir)
        # print(f"{self.robot} | {dir} | {destination}")
        if self.grid[destination] == '[' or self.grid[destination] == ']':
            # Found a robot in destination. Need to make sure
            # it's an optional string of robots and then a empty space

            push_canceled = False
            pushingset = set()
            pushingchars = {}
            q = [ destination ]
            while len(q) > 0 and not push_canceled:
                item = q.pop()

                if item in pushingset:
                    continue
                pushingset.add(item)

                char = self.grid[item]
                pushingchars[item] = char

                if char == '[':
                    q.append(tuple_add( item, (1, 0) ))
                elif char == ']':
                    q.append(tuple_add( item, (-1, 0) ))
                elif char == '#':
                    push_canceled = True
                elif char == '.':
                    pass
                else:
                    raise ValueError("Dunno")

                push_neighbor = tuple_add(item, dir)
                if self.grid[push_neighbor] == '[' or self.grid[push_neighbor] == ']':
                    q.append(push_neighbor)
                elif self.grid[push_neighbor] == '#':
                    push_canceled = True

            if not push_canceled:
                # print("About to push")
                # print(pushingset)
                for loc in pushingset:
                    self.grid[loc] = '.'
                for loc in pushingset:
                    newloc = tuple_add(loc, dir)
                    newchar = pushingchars[loc]
                    self.grid[newloc] = newchar
                self.robot = tuple_add(self.robot, dir)

        elif self.grid[destination] == '.':
            self.robot = destination
        elif self.grid[destination] == '#':
            pass
        else:
            raise ValueError("Something happened")

    def scaleup(self):
        if self.is_scaled:
            raise ValueError("Cannot scale twice")
        self.is_scaled = 1
        newgrid = {}
        newrobot = (-1, -1)

        for y in range(self.max_y):
            xx = 0
            for x in range(self.max_x):
                if self.robot == (x, y):
                    newrobot = (xx, y)

                char = self.grid[(x, y)]
                if char == "#":
                    newgrid[(xx, y)] = '#'
                    xx += 1
                    newgrid[(xx, y)] = '#'
                elif char == "O":
                    newgrid[(xx, y)] = '['
                    xx += 1
                    newgrid[(xx, y)] = ']'
                elif char == ".":
                    newgrid[(xx, y)] = '.'
                    xx += 1
                    newgrid[(xx, y)] = '.'

                xx += 1

        self.grid = newgrid
        self.robot = newrobot
        self.max_x *= 2

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) == self.robot:
                    print("@", end="")
                else:
                    print(self.grid[(x, y)], end="")
            print()
            self.max_y = max(self.max_y, y)

def tuple_add(t1, t2):
    (x1, y1) = t1
    (x2, y2) = t2
    return (x1+x2, y1+y2)

def parse(filename):
    with open(filename) as file:
        string = file.read().strip()
    (maze, dirs) = string.split("\n\n")
    maze = maze.strip()
    dirs = dirs.strip()

    grid = Grid()
    grid.parse_str(maze)
    return grid, dirs

def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

class Day15:
    """AoC 2024 Day 15"""

    @staticmethod
    def part1(filename: str) -> int:
        grid, dirs = parse(filename)
        for char in list(dirs.strip()):
            grid.move_robot(char)
        #grid.display()
        return grid.gps()

    @staticmethod
    def part2(filename: str) -> int:
        grid, dirs = parse(filename)
        grid.scaleup()
        #grid.display()
        i = 0
        for char in list(dirs.strip()):
            i += 1
            # print("Move char", char)
            grid.move_robot2(char)
            # grid.display()
        return grid.gps2()

