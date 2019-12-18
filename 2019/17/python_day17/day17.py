#!/usr/bin/env python

from collections import defaultdict
from aoc.computer import Computer
from aoc.day15 import Day15
from os import system


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


COMPLEX_OF_ROBOTCHAR = {
    "^": complex(0, -1),
    ">": complex(1, 0),
    "v": complex(0, 1),
    "<": complex(-1, 0),
}


def turn_right(direction):
    return direction * complex(0, 1)


def turn_left(direction):
    return direction * complex(0, -1)


class RepairDroid:
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])
        self.grid = defaultdict(lambda: 0)

    def load_pic(self):
        result = self.execute()
        location = complex(0, 0)
        for num in result:
            if num == 10:
                new_imag = int(location.imag + 1)
                location = complex(0, new_imag)
            else:
                char = chr(num)
                self.grid[location] = char
                location += complex(1, 0)

    def execute(self):
        self.cpu.execute()
        result = []
        while self.cpu.has_output():
            result.append(self.cpu.pop_output())
        return result

    def display(self):
        reals = [c.real for c in self.grid.keys() if self.grid[c] != 0]
        imags = [c.imag for c in self.grid.keys() if self.grid[c] != 0]
        system("clear")
        for y in range(int(min(imags)) - 2, int(max(imags)) + 3):
            for x in range(int(min(reals)) - 2, int(max(reals)) + 3):
                char = self.grid[complex(x, y)]
                # print(char, end="")
                if x == 34 and y == 16:
                    print("?", end="")
                else:
                    print(char, end="")
            print("")

    def trace_path(self):
        # print("Trace")
        location, direct = self.robot_location()
        steps = []
        steps_taken = 0
        while True:
            x = int(location.real)
            y = int(location.imag)
            if self.grid[location + direct] != "#":
                # print(f"Need to turn {x} {y}")
                if self.grid[location + turn_right(direct)] == "#":
                    steps.append(steps_taken)
                    steps_taken = 0
                    steps.append("R")
                    direct = turn_right(direct)
                elif self.grid[location + turn_left(direct)] == "#":
                    steps.append(steps_taken)
                    steps_taken = 0
                    steps.append("L")
                    direct = turn_left(direct)
                else:
                    steps.append(steps_taken)
                    # print("Done!")
                    break
            else:
                location += direct
                steps_taken += 1

        # Drop first 0
        steps.pop(0)
        steps2 = []
        # print(steps)
        while len(steps) > 0:
            turn = str(steps.pop(0))
            how_far = str(steps.pop(0))
            steps2.append(turn + how_far)

        # print(location)
        # print(direct)
        # print(steps2)
        return steps2
        # Find location

    def create_program(self):
        trace = self.trace_path()
        print("==========")
        print(trace)
        print("==========")
        # 'R6', 'L12', 'R6', 'R6', 'L12', 'R6', 'L12', 'R6', 'L8', 'L12', 'R12', 'L10', 'L10', 'L12', 'R6', 'L8', 'L12', 'R12', 'L10', 'L10', 'L12', 'R6', 'L8', 'L12', 'R12', 'L10', 'L10', 'L12', 'R6', 'L8', 'L12', 'R6', 'L12', 'R6'

        # A 'R6', 'L12', 'R6',
        # A 'R6', 'L12', 'R6',
        # B 'L12', 'R6', 'L8', 'L12',
        # C 'R12', 'L10', 'L10',
        # B 'L12', 'R6', 'L8', 'L12',
        # C 'R12', 'L10', 'L10',
        # B 'L12', 'R6', 'L8', 'L12',
        # C 'R12', 'L10', 'L10',
        # B 'L12', 'R6', 'L8', 'L12',
        # A 'R6', 'L12', 'R6'

        prog_a = "R,6,L,12,R,6\n"
        prog_b = "L,12,R,6,L,8,L,12\n"
        prog_c = "R,12,L,10,L,10\n"
        prog_main = "A,A,B,C,B,C,B,C,B,A\n"
        everything = (
            self.prog_to_ascii(prog_main)
            + self.prog_to_ascii(prog_a)
            + self.prog_to_ascii(prog_b)
            + self.prog_to_ascii(prog_c)
            + self.prog_to_ascii("n\n")
        )
        return everything

    def prog_to_ascii(self, string):
        return [ord(s) for s in string]

    def robot_location(self):
        reals = [c.real for c in self.grid.keys() if self.grid[c] != 0]
        imags = [c.imag for c in self.grid.keys() if self.grid[c] != 0]
        found_robot = False
        location = complex(-1, -1)
        robot_char = ""
        for y in range(int(min(imags)) - 2, int(max(imags)) + 3):
            for x in range(int(min(reals)) - 2, int(max(reals)) + 3):
                char = self.grid[complex(x, y)]
                if char == "^" or char == "v" or char == "<" or char == ">":
                    location = complex(x, y)
                    robot_char = char
                    found_robot = True
                    break
            if found_robot:
                break

        return location, COMPLEX_OF_ROBOTCHAR[robot_char]

    def part1(self):
        reals = [c.real for c in self.grid.keys() if self.grid[c] != 0]
        imags = [c.imag for c in self.grid.keys() if self.grid[c] != 0]
        intersections = 0
        score = 0
        for y in range(int(min(imags)) - 2, int(max(imags)) + 3):
            for x in range(int(min(reals)) - 2, int(max(reals)) + 3):
                char = self.grid[complex(x, y)]
                if char != "#":
                    continue
                char_n = self.grid[complex(x, y - 1)]
                char_s = self.grid[complex(x, y + 1)]
                char_w = self.grid[complex(x - 1, y)]
                char_e = self.grid[complex(x + 1, y)]
                if char_n == "#" and char_s == "#" and char_w == "#" and char_e == "#":
                    intersections += 1
                    score += x * y

        return score


if __name__ == "__main__":
    program = parse("../../17/input.txt")
    print("Part 1:")
    rd = RepairDroid(program)
    rd.load_pic()
    rd.display()
    print(rd.part1())
    rd.trace_path()

    prog = rd.create_program()

    # Load prog
    cpu = Computer(program, [])
    cpu.memory[0] = 2
    for instruction in prog:
        cpu.add_input(instruction)
    cpu.execute()
    result = []
    while cpu.has_output():
        result.append(cpu.pop_output())
    print("Part 2")
    print(result[-1])
