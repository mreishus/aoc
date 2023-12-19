#!/usr/bin/env python
"""
Advent Of Code 2023 Day 18
https://adventofcode.com/2023/day/18
"""
import re
from collections import defaultdict


class Grid:
    def __init__(self):
        self.digger_loc = (0, 0)
        self.vertices = []
        self.border_distance = 0

    def execute_dig_plan(self, data):
        self.border_distance = 1
        last_direction = None
        for line in data:
            if last_direction != line[0]:
                self.vertices.append(self.digger_loc)
            dx, dy = self.get_direction(line[0])
            distance = int(line[1])

            dx *= distance
            dy *= distance
            self.digger_loc = (self.digger_loc[0] + dx, self.digger_loc[1] + dy)
            self.border_distance += abs(dx) + abs(dy)

    def get_direction(self, direction):
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

    def count_perimeter(self):
        return self.border_distance

    def shoelace_area(self):
        """
        https://en.wikipedia.org/wiki/Shoelace_formula
        """
        area = 0
        for i in range(len(self.vertices) - 1):
            area += (
                self.vertices[i][0] * self.vertices[i + 1][1]
                - self.vertices[i + 1][0] * self.vertices[i][1]
            )
        area += (
            self.vertices[-1][0] * self.vertices[0][1]
            - self.vertices[0][0] * self.vertices[-1][1]
        )
        return abs(area) / 2


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    ## R 6 (#70c710)
    matches = re.match(r"^(\w+)\s+(\d+)\s+(\(\#\w+\))$", line)
    if matches:
        return matches.groups()
    return line


def fix_instructions_p2(data):
    """
    someone swapped the color and instruction parameters when producing the dig plan. They don't have time to fix the bug; one of them asks if you can extract the correct instructions from the hexadecimal codes.

    Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal digits encode the distance in meters as a five-digit hexadecimal number. The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.

    So, in the above example, the hexadecimal codes can be converted into the true instructions:

        #70c710 = R 461937
        #0dc571 = D 56407
        #5713f0 = R 356671
    """
    new_data = []
    for line in data:
        hex_code = line[2][2:-1]
        first_five = hex_code[:-1]
        last = hex_code[-1]
        distance = int(first_five, 16)
        direction = None
        if last == "0":
            direction = "R"
        elif last == "1":
            direction = "D"
        elif last == "2":
            direction = "L"
        elif last == "3":
            direction = "U"
        else:
            raise ValueError(f"Unknown direction: {last}")
        new_data.append((direction, distance, line[2]))
    return new_data


class Day18:
    """AoC 2023 Day 18"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        g = Grid()
        g.execute_dig_plan(data)

        # Pick's theorem https://en.wikipedia.org/wiki/Pick%27s_theorem
        # shoelace_area = I + (B/2) - 1
        # ----------
        # shoelace_area - (B/2) + 1 = I
        # answer = I + B
        # answer = shoelace_area - (B/2) + 1
        # answer = shoelace_area - (B/2) + B + 1
        # answer = shoelace_area + (B/2) + 1
        return int(g.shoelace_area() + g.count_perimeter() / 2 + 1)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        data = fix_instructions_p2(data)
        g = Grid()
        g.execute_dig_plan(data)

        # Pick's theorem https://en.wikipedia.org/wiki/Pick%27s_theorem
        return int(g.shoelace_area() + g.count_perimeter() / 2 + 1)
