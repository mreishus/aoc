#!/usr/bin/env python
"""
Advent Of Code 2024 Day 4
https://adventofcode.com/2024/day/4
"""
import re

class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[(x, y)] = char
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def part1(self):
        lines = []

        # horizontal left to right and right to left
        for y in range(self.max_y):
            line = [ self.grid[(x, y)] for x in range(self.max_x) ]
            lines.append( ''.join(line) )
            lines.append( ''.join(reversed(line)) )

        # vertical up to down and down to up
        for x in range(self.max_x):
             line = [ self.grid[(x, y)] for y in range(self.max_y) ]
             lines.append( ''.join(line) )
             lines.append( ''.join(reversed(line)) )

        # diag top left to bottom right, and reversed - top edge start
        for start_x in range(self.max_x):
            start_y = 0
            this_line = []
            for xx, yy in self.go_downright(start_x, start_y):
                this_line.append(self.grid[(xx, yy)])
            lines.append( ''.join(this_line) )
            lines.append( ''.join(reversed(this_line)) )

        # diag top left to bottom right, and reversed - left edge start
        for start_y in range(self.max_y):
            if start_y == 0:
                continue
            start_x = 0
            this_line = []
            for xx, yy in self.go_downright(start_x, start_y):
                this_line.append(self.grid[(xx, yy)])
            lines.append( ''.join(this_line) )
            lines.append( ''.join(reversed(this_line)) )

        # diag top right to bottom left, and reversed - top edge start
        for start_x in range(self.max_x):
            start_y = 0
            this_line = []
            for xx, yy in self.go_downleft(start_x, start_y):
                this_line.append(self.grid[(xx, yy)])
            lines.append( ''.join(this_line) )
            lines.append( ''.join(reversed(this_line)) )

        # diag top right to bottom left, and reversed - right edge start
        for start_y in range(self.max_y):
            if start_y == 0:
                continue
            start_x = self.max_x - 1
            this_line = []
            for xx, yy in self.go_downleft(start_x, start_y):
                this_line.append(self.grid[(xx, yy)])
            lines.append( ''.join(this_line) )
            lines.append( ''.join(reversed(this_line)) )

        count = 0
        pattern = r'XMAS'
        for line in lines:
            matches = re.findall(pattern, line)
            count += len(matches)
        return count

    def part2(self):
        found_count = 0
        for x in range(self.max_x):
            for y in range(self.max_y):
                # Verify all points are within the grid
                if not (x + 2, y + 2) in self.grid:
                    continue

                # Verify center is A
                if self.grid[(x+1, y+1)] != 'A':
                    continue

                slash_one_a = self.grid[(x, y)]
                slash_one_b = self.grid[(x+2, y+2)]

                v = (slash_one_a == 'M' and slash_one_b == 'S') or (slash_one_a == 'S' and slash_one_b == 'M')
                if not v:
                    continue

                slash_two_a = self.grid[(x+2, y)]
                slash_two_b = self.grid[(x, y+2)]

                v = (slash_two_a == 'M' and slash_two_b == 'S') or (slash_two_a == 'S' and slash_two_b == 'M')
                if not v:
                    continue

                found_count += 1
        return found_count

    def go_downright(self, x, y):
        size = max( self.max_x, self.max_y )
        for d in range(size):
            if (x + d, y + d) in self.grid:
                yield (x + d, y + d)
            else:
                break

    def go_downleft(self, x, y):
        size = max( self.max_x, self.max_y )
        for d in range(size):
            if (x - d, y + d) in self.grid:
                yield (x - d, y + d)
            else:
                break


class Day04:
    """AoC 2024 Day 04"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.part1()

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.part2()
