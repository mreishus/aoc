#!/usr/bin/env python
"""
Main program runner for Advent of Code 2020 in Python.
This is a series of programming problems available at https://adventofcode.com/2020
"""
from aoc.day01 import Day01


def day1to5():
    """ Solves 2020 days 1 - 5. """
    ## Day 1
    print("2020 Day 01 Part 1:", end=" ")
    print(Day01.part1("../inputs/01/input.txt"))
    print("2020 Day 01 Part 2:", end=" ")
    print(Day01.part2("../inputs/01/input.txt"))


def latest():
    """ Scratchpad to work on. """
    pass


if __name__ == "__main__":
    day1to5()
    latest()
