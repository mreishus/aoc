#!/usr/bin/env python

from collections import defaultdict
from aoc.computer import Computer, solve1
from aoc.day19 import Day19


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


class Day21:
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])
        self.grid = defaultdict(lambda: "?")
        self.filled_squares = {}

    def run(self):
        self.cpu.execute()
        result = []
        while self.cpu.has_output():
            result.append(self.cpu.pop_output())
        self.display(result)

    def display(self, result):
        print("\n")
        for char in result:
            if char < 255:
                print(chr(char), end="")
            else:
                print(char)

    def send(self, string):
        prog = self.prog_to_ascii(string)
        for instruction in prog:
            self.cpu.add_input(instruction)

    def prog_to_ascii(self, string):
        return [ord(s) for s in string]


if __name__ == "__main__":
    program = parse("../../21/input.txt")
    # print(program)
    d21 = Day21(program)
    d21.run()
    this_prog = [
        # (J) Jump if (C3) is missing and (D4) is filled
        #  - But not if E(5) and H8 are missing
        #  1. Fill J with E5 present or H5 present
        "NOT E J",
        "NOT J J",
        "OR H J",
        #  2. Fill T with C3 missing and D4 filled
        "NOT C T",
        "AND D T",
        # 3. Move T to J somehow
        "AND T J",
        # Also jump if A(1) is missing
        "NOT A T",
        "OR T J",
        # Also jump if A(2) is missing and D4 is filled  (Probably need to add somethign here)
        "NOT B T",
        "AND D T",
        "OR T J",
        "RUN"
    ]

    d21.send("\n".join(this_prog) + "\n")
    d21.run()
