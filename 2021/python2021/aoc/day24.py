#!/usr/bin/env python
"""
Advent Of Code 2021 Day 24
https://adventofcode.com/2021/day/24
"""
import random

PRINT_LOG = False


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    inst = line.split()
    if len(inst) == 3 and inst[2].lstrip("-").isdigit():
        inst = (inst[0], inst[1], int(inst[2]))
    return inst


class Computer:
    def __init__(self, program, inputs):
        self.program = program
        self.inputs = inputs
        self.pc = 0
        self.vars = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }
        self.equalsum = 0
        self.equallog = []

    def lookup(self, a):
        if isinstance(a, int):
            return a
        return self.vars[a]

    def run(self):
        while self.pc < len(self.program):
            instruction, *args = self.program[self.pc]
            if instruction == "inp":
                this_input = self.inputs.pop(0)
                self.vars[args[0]] = this_input
            elif instruction == "add":
                value = self.lookup(args[0]) + self.lookup(args[1])
                dest = args[0]
                self.vars[dest] = value
            elif instruction == "mul":
                value = self.lookup(args[0]) * self.lookup(args[1])
                dest = args[0]
                self.vars[dest] = value
            elif instruction == "div":
                value = self.lookup(args[0]) // self.lookup(args[1])
                dest = args[0]
                self.vars[dest] = value
            elif instruction == "mod":
                value = self.lookup(args[0]) % self.lookup(args[1])
                dest = args[0]
                self.vars[dest] = value
            elif instruction == "eql":
                dest = args[0]
                value = 1 if self.lookup(args[0]) == self.lookup(args[1]) else 0
                if PRINT_LOG:
                    print(
                        f"EQL {args[0]} {args[1]} | {self.lookup(args[0])} == {self.lookup(args[1])} -> {value}"
                    )
                self.equallog.append(
                    f"EQL {args[0]} {args[1]} | {self.lookup(args[0])} == {self.lookup(args[1])} -> {value}"
                )
                self.equallog.append(
                    f" {self.vars['w']} {self.vars['x']} {self.vars['y']} {self.vars['z']} "
                )
                if value == 1 and args[1] != 0:
                    self.equalsum += 1
                self.vars[dest] = value
            self.pc += 1
        return self.vars


class Day24:
    """AoC 2021 Day 24"""

    @staticmethod
    def part1(filename: str) -> int:
        """Given a filename, solve 2021 day 24 part 1"""
        data = parse(filename)
        inputs = []

        def check_model(inputs):
            cpu = Computer(data, list(inputs))
            cpuvars = cpu.run()
            if False and cpu.equalsum > 2:
                print(inputs)
                print(f"SUM: {cpu.equalsum}")
                for line in cpu.equallog:
                    print(line)
                print(cpuvars)
            print(f" {inputs} {cpuvars} ")
            return cpuvars["z"] == 1

        # This was done by hand, look at notes in input.copy.txt
        digits = [9, 2, 9, 2, 8, 9, 1, 4, 9, 9, 9, 9, 9, 1]
        digits = [9, 1, 8, 1, 1, 2, 1, 1, 6, 1, 1, 9, 8, 1]
        #         1  2  3  4  5  6  7  8  9 10 11 12 13 14
        # d4 = d3 - 7       ********
        # d6 = d5 + 1       ********
        # d9 = d8 + 5       *******
        # d11 = d10         ********
        # d12 = d7 + 8      *********
        # d13 = d2 + 7      **********
        # d14 = d1 - 8      *************
        global PRINT_LOG
        PRINT_LOG = False
        print("")
        check_model(digits)
        return -1

        # ---> [6, 7, 2, 7, 4, 1, 8, 1, 6, 2, 7, 7, 7, 5] <---
        for i in range(50000):
            digits = [random.randint(1, 9) for _ in range(14)]
            # digits[9] = 6
            result = check_model(digits)
            if result:
                print("WINNER")
                print(f"---> {digits} <---")
                exit("FOUND RESULT")
        return -1

    @staticmethod
    def part2(filename: str) -> int:
        """Given a filename, solve 2021 day 24 part 2"""
        data = parse(filename)
        if len(data) < 20:
            print(data)
        return -1


# if __name__ == "__main__":
#     print(Day24.part1("../inputs/24/input.txt"))
