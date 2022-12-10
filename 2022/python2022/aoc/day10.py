#!/usr/bin/env python
"""
Advent Of Code 2022 Day 10
https://adventofcode.com/2022/day/10
"""
from collections import defaultdict


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    if line == "noop":
        return [line, 0]
    cmd, arg = line.split(" ")
    return [cmd, int(arg)]


class Day10:
    """AoC 2022 Day 10"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        schedule = defaultdict(int)

        data.append(["noop", 0])
        data.append(["noop", 0])

        x = 1
        cycle = 0
        opcode = None
        val = 0
        time_remaining = 1
        max_cycles = len(data) + 3
        max_cycles = 221
        answer = 0
        for cycle in range(max_cycles):
            # print(f"Cycle {cycle} X {x}")

            # If the current cycle number is one of the ones we're interested in,
            # calculate the signal strength and print it
            if cycle in [20, 60, 100, 140, 180, 220]:
                signal_strength = cycle * x
                answer += signal_strength
                print(f"Signal strength during cycle {cycle}: {signal_strength} ")

            cycle += 1
            time_remaining -= 1

            if time_remaining == 0:
                if opcode == "addx":
                    x += val

                ## Get new instruction
                if len(data) > 0:
                    opcode, val = data.pop(0)
                    if opcode == "noop":
                        time_remaining = 1
                    elif opcode == "addx":
                        time_remaining = 2
                else:
                    print("Can't get opcode")

        return answer

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        if len(data) <= 20:
            print(data)
        return -2
