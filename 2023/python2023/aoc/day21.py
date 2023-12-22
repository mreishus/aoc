#!/usr/bin/env python
"""
Advent Of Code 2023 Day 21
https://adventofcode.com/2023/day/21
"""
from collections import deque
import numpy as np


class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.start = None

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    if char == "S":
                        self.start = (x, y)
                        char = "."
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

    def display_with_visited(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) in self.finish_locations:
                    print("O", end="")
                else:
                    print(self.grid[(x, y)], end="")
            print()

    def bfs(self, start=None, max_dist=6):
        if start is None:
            start = self.start
        if start is None:
            raise Exception("No start location")

        start = (start[0], start[1], 0, 0)
        visited = set()
        finish_locations = set()
        queue = deque([(start, 0)])
        i = 0
        while queue:
            i += 1
            loc, dist = queue.pop()
            if i % 500000 == 0:
                print(loc, dist, " | ", len(queue), len(visited), len(finish_locations))
            if (loc, dist) not in visited:
                visited.add((loc, dist))
                if dist == max_dist:
                    finish_locations.add(loc)

                if dist < max_dist:
                    for n in self.get_neighbors(loc):
                        if (n, dist + 1) in visited:
                            continue
                        queue.append((n, dist + 1))
        self.visited = visited
        self.finish_locations = finish_locations
        return finish_locations

    def get_neighbors(self, node):
        neighbors = []
        x, y, x_quot, y_quot = node
        possibilities = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        for xx, yy in possibilities:
            ## x wrap around: xx = xx % self.max_x
            ## y wrap around: yy = yy % self.max_y
            this_x_quot = x_quot
            this_y_quot = y_quot
            if xx < 0:
                this_x_quot -= 1
            elif xx >= self.max_x:
                this_x_quot += 1
            if yy < 0:
                this_y_quot -= 1
            elif yy >= self.max_y:
                this_y_quot += 1
            xx = xx % self.max_x
            yy = yy % self.max_y
            if (xx, yy) in self.grid and self.grid[(xx, yy)] != "#":
                neighbors.append((xx, yy, this_x_quot, this_y_quot))
        return neighbors


class Day21:
    """AoC 2023 Day 21"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        # g.display()
        x = g.bfs(None, 64)
        return len(x)

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        # g.display()

        points = []
        ## Had to spoil myself on this solution
        # g.start = (65, 65)
        # g.max_x, g.max_y = 131, 131
        # Each row/column is a straight shot to the next grid w/ no obstacles
        # Our search expands in a diamond shape, so it's a quadratic equation
        for i in [65, 65 + 131, 65 + 131 + 131]:
            z = g.bfs(None, i)
            print(f"{i}: Found {len(z)} locations")
            new_point = [i, len(z)]
            points.append(new_point)

        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]

        A = np.array([[x1**2, x1, 1], [x2**2, x2, 1], [x3**2, x3, 1]])
        b = np.array([y1, y2, y3])

        # Solving the system of equations
        a, b, c = np.linalg.solve(A, b)
        # print(f"The quadratic equation is: f(x) = {a}x^2 + {b}x + {c}")

        def estimate_point(x):
            return int(a * x**2 + b * x + c)

        return estimate_point(26501365)
