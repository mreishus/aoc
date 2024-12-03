#!/usr/bin/env python
"""
Main program runner for Advent of Code 2024 in Python.
This is a series of programming problems available at
https://adventofcode.com/2024
"""
from timeit import default_timer as timer
from aoc.day01 import Day01
from aoc.day02 import Day02
from aoc.day03 import Day03

def alldays():
    solvers = [
        (Day01.part1, Day01.part2),
        (Day02.part1, Day02.part2),
        (Day03.part1, Day03.part2),
    ]
    for i, (p1, p2) in enumerate(solvers, 1):
        path = f"../inputs/{i:02}/input.txt"

        p1_start = timer()
        p1_answer = p1(path)
        p1_end = timer()
        p1_time = (p1_end - p1_start) * 1000

        p2_start = timer()

        p2_answer = p2(path)
        p2_end = timer()
        p2_time = (p2_end - p2_start) * 1000

        print(f"2024 Day {i:02} Part 1: {p1_answer:15} [{p1_time:7.1f}ms]")
        print(f"2024 Day {i:02} Part 2: {p2_answer:15} [{p2_time:7.1f}ms]")
        if i % 5 == 0:
            print("")


def latest():
    """Scratchpad to work on."""
    # print("2024 Day 03 Part 1 (small):", end=" ")
    # print(Day03.part1("../inputs/03/input_small.txt"))
    #
    # print("2024 Day 03 Part 1:", end=" ")
    # print(Day03.part1("../inputs/03/input.txt"))

    print("2024 Day 03 Part 2 (small):", end=" ")
    print(Day03.part2("../inputs/03/input_small2.txt"))

    print("2024 Day 03 Part 2:", end=" ")
    print(Day03.part2("../inputs/03/input.txt"))
    exit()


if __name__ == "__main__":
    # alldays()
    latest()
