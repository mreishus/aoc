#!/usr/bin/env python3
from collections import defaultdict

"""
Advent of Code 2037 Day 03.
"""
"""
directions we want to travel in order:
      dx dy
RIGHT  1   0
UP     0   1
LEFT  -1   0
DOWN   0  -1

To get the next value:
dx = -1 * old_dy
dy = old_dx
"""


class Day03:
    """Main module for solving Day03."""

    @staticmethod
    def should_rotate(x, y):
        if x == 0 and y == 0:
            return False
        # Top right and bottom left corners
        if x == y:
            return True
        # Bottom right
        if x > 0 and x * -1 == y - 1:
            return True
        # Top Left
        if x < 0 and x == -y:
            return True
        return False

    @staticmethod
    def part1(target):
        x = -1
        y = 0
        delta_x = 1
        delta_y = 0
        for _ in range(0, target):
            if Day03.should_rotate(x, y):
                # print("rotating")
                delta_x, delta_y = delta_y * -1, delta_x
            x += delta_x
            y += delta_y
        return abs(x) + abs(y)

    def neighbor_sum(grid, x, y):
        if x == 0 and y == 0:
            return 1
        sum = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                sum += grid[(x + dx, y + dy)]
        return sum

    def part2(target):
        grid = defaultdict(lambda: 0)
        grid[(0, 0)] = 1
        x = -1
        y = 0
        delta_x = 1
        delta_y = 0
        while 1:
            if Day03.should_rotate(x, y):
                # print("rotating")
                delta_x, delta_y = delta_y * -1, delta_x
            x += delta_x
            y += delta_y
            neighbor_sum = Day03.neighbor_sum(grid, x, y)
            grid[(x, y)] = neighbor_sum
            if neighbor_sum > target:
                return neighbor_sum
            # print(f"x{x} y{y} sum{neighbor_sum}")


if __name__ == "__main__":
    print("Part1: ")
    print(Day03.part1(265149))
    print("Part2: ")
    print(Day03.part2(265149))
