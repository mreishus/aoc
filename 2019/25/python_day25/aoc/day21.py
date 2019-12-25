#!/usr/bin/env python

from aoc.computer import Computer


class Day21:
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])

    def reset(self):
        self.cpu = Computer(self.program, [])

    def execute(self):
        self.cpu.execute()
        result = []
        while self.cpu.has_output():
            result.append(self.cpu.pop_output())
        self.display(result)

    def execute_silent(self):
        self.cpu.execute()
        result = []
        while self.cpu.has_output():
            result.append(self.cpu.pop_output())
        return result

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

    def run_springscript_interactive(self, prog_string_array):
        """ Runs springscript and prints to console. """
        self.reset()
        self.execute()
        self.send("\n".join(prog_string_array) + "\n")
        self.execute()

    def run_springscript_headless(self, prog_string_array):
        """ Runs springscript and returns the last output. """
        self.reset()
        self.execute_silent()
        self.send("\n".join(prog_string_array) + "\n")
        output = self.execute_silent()
        return output[-1]

    def part1(self):
        # This program was derived manually (as intended, I suspect)
        # Jump if (NOT A1) OR (NOT C AND D)
        part1_prog = ["NOT C J", "AND D J", "NOT A T", "OR T J", "WALK"]
        # self.run_springscript_interactive(part1_prog)
        return self.run_springscript_headless(part1_prog)

    def part2(self):
        # This program was derived manually (as intended, I suspect)
        part2_prog = [
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
            "RUN",
        ]
        # self.run_springscript_interactive(part2_prog)
        return self.run_springscript_headless(part2_prog)
