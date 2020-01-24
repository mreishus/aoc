#!/usr/bin/env python
"""
Advent Of Code 2015 Day 2
https://adventofcode.com/2015/day/2
"""

def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]

def parse_line(line: str):
    [length, width, height] = [int(num) for num in line.split("x")]
    return Present(length, width, height)

class Present():
    """Docstring for Present. """
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def paper_required(self) -> int:
        l = self.length
        w = self.width
        h = self.height
        sides = [2*l*w, 2*w*h, 2*h*l]
        slack = min(sides) // 2
        return sum(sides) + slack

    def ribbon(self) -> int:
        return self.smallest_perimeter() + self.volume()

    def smallest_perimeter(self) -> int:
        sides = [self.length, self.width, self.height]
        smallest_two_sides = sorted(sides)[0:2]
        return sum(smallest_two_sides) * 2

    def volume(self) -> int:
        return self.length * self.width * self.height

class Day02:
    """ AoC 2015 Day 02 """
    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 02 part 1 """
        data = parse(filename)
        return sum(p.paper_required() for p in data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 21 part 2 """
        data = parse(filename)
        return sum(p.ribbon() for p in data)
