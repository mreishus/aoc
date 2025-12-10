#!/usr/bin/env python
"""
Advent Of Code 2025 Day 9
https://adventofcode.com/2025/day/9
"""
from collections import defaultdict

def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip().split("\n")
    r = []
    for line in lines:
        r.append(tuple(map(int, line.split(","))))
    return r

class Grid:
    def __init__(self):
        self.z = []
        self.hori_lines = []
        self.vert_lines = []

    def solve2(self, data):
        l = len(data)
        grid = defaultdict(lambda: ".")

        min_x = None
        min_y = None
        max_x = None
        max_y = None

        for i in range(l):
            j = (i+1) % l
            self.draw_line(grid, data[i], data[j])
            (x, y) = data[i]
            if min_x is None or max_x is None:
                min_x = x
                max_x = x
            if min_y is None or max_y is None:
                min_y = y
                max_y = y
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        for x, y in data:
            grid[(x,y)] = '#'

        max_area = 0
        for i in range(len(data)):
            x, y = data[i]
            for j in range(i+1, len(data)):
                xx, yy = data[j]

                if not self.eligible( x, y, xx, yy):
                    continue

                area = (abs(x - xx) + 1) * (abs(y - yy) + 1)
                if area > max_area:
                    max_area = area

        return max_area

    def draw_line(self, grid, pair1, pair2):
        (x, y) = pair1
        (xx, yy) = pair2
        if y == yy:
            small = min(x, xx)
            large = max(x, xx)
            self.hori_lines.append(((small, y), (large, y)))
            for this_x in range(small, large+1):
                grid[(this_x, y)] = '-'
        elif x == xx:
            small = min(y, yy)
            large = max(y, yy)
            self.vert_lines.append(((x, small), (x, large)))
            for this_y in range(small, large+1):
                grid[(x, this_y)] = '|'
        else:
            raise ValueError("Bad")

    def eligible(self, x, y, xx, yy):
        if x > xx:
            x,xx = xx,x
        if y > yy:
            y,yy = yy,y

        # Do any lines in self.hori_lines pass through our vertical lines?
        for [(a, b), (aa, bb)] in self.hori_lines:
            # Reminder: b == bb since they're all hori_lines
            if b > y and b < yy:
                # The line can end at my left edge, but it can't start there
                if a <= x < aa:
                    return False
                if a < xx <= aa:
                    return False

        # Do any lines in self.vert_lines pass through our horizontal lines?
        for [(a, b), (aa, bb)] in self.vert_lines:
            # Reminder: a == aa since they're all vert_lines
            if a > x and a < xx:
                # The line can end at my top edge, but it can't start there
                if b <= y < bb:
                    return False
                if b < yy <= bb:
                    return False
        return True

def display(grid, data=None, i=None, j=None):
    highlights = {}
    if data and i is not None:
        highlights[tuple(data[i])] = 'I'
    if data and j is not None:
        highlights[tuple(data[j])] = 'J'
    
    all_x = [p[0] for p in grid.keys()]
    all_y = [p[1] for p in grid.keys()]
    
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in highlights:
                row += highlights[(x, y)]
            else:
                row += grid[(x, y)]
        print(row)

class Day09:
    """AoC 2025 Day 09"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        max_area = 0
        for i in range(len(data)):
            x, y = data[i]
            for j in range(i+1, len(data)):
                xx, yy = data[j]
                area = (abs(x - xx) + 1) * (abs(y - yy) + 1)
                if area > max_area:
                    max_area = area
        return max_area

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        g = Grid()
        # Too high:            1983520000
        # Too low:               49424904
        # Incorrect but close: 1518370134
        return g.solve2(data)

