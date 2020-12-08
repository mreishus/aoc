#!/usr/bin/env python
"""
Advent Of Code 2020 Day 7
https://adventofcode.com/2020/day/7
"""


def parse(filename):
    with open(filename) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def parse_line(line):
    (left, right) = line.split(" ")
    right = int(right)
    return (left, right)


class Computer:
    def __init__(self, program):
        self.pc = 0
        self.program = program
        self.acc = 0

    def find_acc_before_infinite_loop(self):
        seen = set()
        while self.pc not in seen:
            seen.add(self.pc)
            self.step()
        return self.acc

    def infinite_loop_or_terminate(self):
        seen = set()
        while True:
            if self.pc in seen:
                return ("infinite", self.acc)
            if self.pc >= len(self.program):
                return ("terminate", self.acc)
            seen.add(self.pc)
            self.step()

    def step(self):
        (inst, val) = self.program[self.pc]
        if inst == "nop":
            self.pc += 1
        elif inst == "acc":
            self.acc += val
            self.pc += 1
        elif inst == "jmp":
            self.pc += val


class Day08:
    """ AoC 2020 Day 08 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 08 part 1 """
        data = parse(filename)
        cpu = Computer(data)
        return cpu.find_acc_before_infinite_loop()

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 08 part 2 """
        data = parse(filename)
        for (i, (inst, val)) in enumerate(data):
            if inst not in ("nop", "jmp"):
                continue

            new_prog = data.copy()
            new_inst = "jmp" if inst == "nop" else "nop"
            new_prog[i] = (new_inst, val)

            cpu = Computer(new_prog)
            (state, acc) = cpu.infinite_loop_or_terminate()

            if state == "terminate":
                return acc
        return None
