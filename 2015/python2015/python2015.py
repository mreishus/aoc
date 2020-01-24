#!/usr/bin/env python
"""
Main program runner for Advent of Code 2015 in Python.
This is a series of programming problems available at https://adventofcode.com/2015
"""
from aoc.day01 import Day01

def main():
    print("2015 Day 01 Part 1:", end=" ")
    print(Day01.part1("../inputs/01/input.txt"))
    print("2015 Day 01 Part 2:", end=" ")
    print(Day01.part2("../inputs/01/input.txt"))

if __name__ == "__main__":
    main()
