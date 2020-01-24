#!/usr/bin/env python
"""
Advent Of Code 2015 Day 1
https://adventofcode.com/2015/day/1
"""

def parse(filename: str) -> str:
    """ Given a filename, returns the first line of a file. """
    with open(filename) as file:
        return file.readline().strip()

def floor(data: str) -> int:
    """ Given a string like "))())", determines the resulting floor,
    After moving after moving through all characters.
    Each ( moves up one floor. Each ) moves down one floor. """
    level = 0
    for char in data:
        if char == "(":
            level += 1
        elif char == ")":
            level -= 1
        else:
            raise ValueError("Unknown chat")
    return level

def index_of_floor(data: str, target_floor: int) -> int:
    """ Given a string like "))())", find the index of the first
    character that brings the elevator to position `target_floor`.
    Each ( moves up one floor. Each ) moves down one floor. """
    level = 0
    for (i, char) in enumerate(data, 1):
        if char == "(":
            level += 1
        elif char == ")":
            level -= 1
        else:
            raise ValueError("Unknown chat")
        if level == target_floor:
            return i
    return None

class Day01:
    """ AoC 2015 Day 01 """
    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 01 part 1 """
        data = parse(filename)
        return floor(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 01 part 2 """
        data = parse(filename)
        return index_of_floor(data, -1)
