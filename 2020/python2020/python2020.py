#!/usr/bin/env python
"""
Main program runner for Advent of Code 2020 in Python.
This is a series of programming problems available at https://adventofcode.com/2020
"""
from aoc.day01 import Day01
from aoc.day02 import Day02
from aoc.day03 import Day03
from aoc.day04 import Day04
from aoc.day05 import Day05
from aoc.day06 import Day06
from aoc.day07 import Day07
from aoc.day08 import Day08


def day1to5():
    """ Solves 2020 days 1 - 5. """
    ## Day 1
    print("2020 Day 01 Part 1:", end=" ")
    print(Day01.part1("../inputs/01/input.txt"))
    print("2020 Day 01 Part 2:", end=" ")
    print(Day01.part2("../inputs/01/input.txt"))
    ## Day 2
    print("2020 Day 02 Part 1:", end=" ")
    print(Day02.part1("../inputs/02/input.txt"))
    print("2020 Day 02 Part 2:", end=" ")
    print(Day02.part2("../inputs/02/input.txt"))
    ## Day 3
    print("2020 Day 03 Part 1:", end=" ")
    print(Day03.part1("../inputs/03/input.txt"))
    print("2020 Day 03 Part 2:", end=" ")
    print(Day03.part2("../inputs/03/input.txt"))
    ## Day 4
    print("2020 Day 04 Part 1:", end=" ")
    print(Day04.part1("../inputs/04/input.txt"))
    print("2020 Day 04 Part 2:", end=" ")
    print(Day04.part2("../inputs/04/input.txt"))
    ## Day 5
    print("2020 Day 05 Part 1:", end=" ")
    print(Day05.part1("../inputs/05/input.txt"))
    print("2020 Day 05 Part 2:", end=" ")
    print(Day05.part2("../inputs/05/input.txt"))


def day6to10():
    ## Day 6
    print("2020 Day 06 Part 1:", end=" ")
    print(Day06.part1("../inputs/06/input.txt"))
    print("2020 Day 06 Part 2:", end=" ")
    print(Day06.part2("../inputs/06/input.txt"))
    ## Day 7
    print("2020 Day 07 Part 1:", end=" ")
    print(Day07.part1("../inputs/07/input.txt"))
    print("2020 Day 07 Part 2:", end=" ")
    print(Day07.part2("../inputs/07/input.txt"))


def latest():
    """ Scratchpad to work on. """
    ## Day 7
    print("2020 Day 08 Part 1 (small 1):", end=" ")
    print(Day08.part1("../inputs/08/input_small_1.txt"))
    print("2020 Day 08 Part 1:", end=" ")
    print(Day08.part1("../inputs/08/input.txt"))

    print("")
    print("--")
    print("")

    print("2020 Day 08 Part 2 (small 1):", end=" ")
    print(Day08.part2("../inputs/08/input_small_1.txt"))
    print("2020 Day 08 Part 2 (small 2):", end=" ")
    print(Day08.part2("../inputs/08/input_small_2.txt"))
    print("2020 Day 08 Part 2:", end=" ")
    print(Day08.part2("../inputs/08/input.txt"))


if __name__ == "__main__":
    # day1to5()
    # day6to10()
    latest()
