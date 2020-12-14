#!/usr/bin/env python
"""
Main program runner for Advent of Code 2020 in Python.
This is a series of programming problems available at https://adventofcode.com/2020
"""
from timeit import default_timer as timer
from aoc.day01 import Day01
from aoc.day02 import Day02
from aoc.day03 import Day03
from aoc.day04 import Day04
from aoc.day05 import Day05
from aoc.day06 import Day06
from aoc.day07 import Day07
from aoc.day08 import Day08
from aoc.day09 import Day09
from aoc.day10 import Day10
from aoc.day11 import Day11
from aoc.day12 import Day12
from aoc.day13 import Day13
from aoc.day14 import Day14


def alldays():
    solvers = [
        (Day01.part1, Day01.part2),
        (Day02.part1, Day02.part2),
        (Day03.part1, Day03.part2),
        (Day04.part1, Day04.part2),
        (Day05.part1, Day05.part2),
        (Day06.part1, Day06.part2),
        (Day07.part1, Day07.part2),
        (Day08.part1, Day08.part2),
        (
            lambda filename: Day09.part1(filename, 25),
            lambda filename: Day09.part2(filename, 25),
        ),
        (Day10.part1, Day10.part2),
        (Day11.part1, Day11.part2),
        (Day12.part1, Day12.part2),
        (Day13.part1, Day13.part2),
    ]
    for (i, (p1, p2)) in enumerate(solvers, 1):
        path = f"../inputs/{i:02}/input.txt"

        p1_start = timer()
        p1_answer = p1(path)
        p1_end = timer()
        p1_time = (p1_end - p1_start) * 1000

        p2_start = timer()
        p2_answer = p2(path)
        p2_end = timer()
        p2_time = (p2_end - p2_start) * 1000

        print(f"2020 Day {i:02} Part 1: {p1_answer:15} [{p1_time:6.1f}ms]")
        print(f"2020 Day {i:02} Part 2: {p2_answer:15} [{p2_time:6.1f}ms]")


def latest():
    """ Scratchpad to work on. """
    ## Day 14
    print("2020 Day 14 Part 1 (small1):", end=" ")
    print(Day14.part1("../inputs/14/input_small_1.txt"))
    print("2020 Day 14 Part 1:", end=" ")
    print(Day14.part1("../inputs/14/input.txt"))
    # print("---")
    # print("2020 Day 14 Part 2 (small1):", end=" ")
    # print(Day14.part2("../inputs/14/input_small_1.txt"))
    # print("2020 Day 14 Part 2:", end=" ")
    # print(Day14.part2("../inputs/14/input.txt"))


if __name__ == "__main__":
    # alldays()
    latest()
