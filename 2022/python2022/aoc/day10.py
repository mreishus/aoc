#!/usr/bin/env python
"""
Advent Of Code 2022 Day 10
https://adventofcode.com/2022/day/10
"""


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    if " " in line:
        cmd, arg = line.split(" ")
        return [cmd, int(arg)]
    return [line, 0]


def solve(data, do_print=False):
    x = 1
    opcode = None
    t = 1
    val, cycle, answer, signal_strength = 0, 0, 0, 0
    print("")
    for _ in range(0, 240):
        if cycle in [20, 60, 100, 140, 180, 220]:
            signal_strength = cycle * x
            answer += signal_strength

        if do_print:
            fixed_cycle = cycle % 40
            if fixed_cycle in [x, x + 1, x + 2]:
                print("#", end="")
            else:
                print(" ", end="")

            if cycle % 40 == 0:
                print("]", end="")
                print("")

        cycle += 1
        t -= 1
        if t > 0:
            continue

        if opcode == "addx":
            x += val

        ## Get new instruction
        if len(data) > 0:
            opcode, val = data.pop(0)
            if opcode == "noop":
                t = 1
            elif opcode == "addx":
                t = 2

    return answer


class Day10:
    """AoC 2022 Day 10"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return solve(data)

    @staticmethod
    def part2(filename: str) -> str:
        data = parse(filename)
        solve(data, True)
        return "\nSee above"
