#!/usr/bin/env python

from itertools import permutations
from collections import defaultdict
from os import system
import sys

# DEBUG = True
DEBUG = False


class OP:
    ADD = 1
    MULT = 2
    SAVE = 3
    WRITE = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    SET_REL_BASE = 9
    STOP = 99


class MODE:
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


def digit_from_right(x, n):
    return x // (10 ** n) % 10


class Computer(object):
    def __init__(self, memory, inputs):
        self.memory = defaultdict(lambda: 0)
        for i, k in enumerate(memory):
            self.memory[i] = k
        self.inputs = inputs.copy()
        self.outputs = []
        self.pc = 0
        self.state = "new"
        self.relative_base = 0

    def direct(self, n):
        """ Get the direct value of the memory address of the Nth arg, or PC + N"""
        return self.memory[self.pc + n]

    def lookup(self, n):
        """ Get the dereferenced value of the Nth arg, after checking the Nth mode
        of the current instruction. """
        instruction = self.memory[self.pc]
        # If instruction is 105, and n=1, mode is the "1", or the 2nd digit
        # from right 0 indexed (3rd when counting naturally)
        mode = digit_from_right(instruction, n + 1)
        if mode == MODE.POSITION:
            return self.memory[self.direct(n)]
        if mode == MODE.IMMEDIATE:
            return self.direct(n)
        if mode == MODE.RELATIVE:
            # Like position, but counts from relative base
            address = self.direct(n) + self.relative_base
            return self.memory[address]
        raise Exception("Unknown mode")

    def lookup_left(self, n):
        """ Use on left side of equals only (needs better explanation) """
        instruction = self.memory[self.pc]
        mode = digit_from_right(instruction, n + 1)
        if mode == MODE.POSITION:
            return self.direct(n)
        if mode == MODE.IMMEDIATE:
            return self.direct(n)
        if mode == MODE.RELATIVE:
            return self.direct(n) + self.relative_base

    def info(self, string):
        if DEBUG:
            print(string)

    def add_input(self, x):
        self.inputs.append(x)

    def has_output(self):
        return len(self.outputs) > 0

    def pop_output(self):
        return self.outputs.pop(0)

    def execute(self):
        if self.state == "halted":
            print("Refusing to execute; is halted")
        self.state = "running"
        while True:
            instruction = self.memory[self.pc] % 100
            # print(self.memory[self.pc])
            if instruction == OP.ADD:
                self.memory[self.lookup_left(3)] = self.lookup(1) + self.lookup(2)
                self.info(
                    f"    -> ADD program[{self.direct(3)}] = {self.lookup(1)} + {self.lookup(2)} = {self.lookup(1) + self.lookup(2)}"
                )
                self.pc += 4
            elif instruction == OP.MULT:
                self.memory[self.lookup_left(3)] = self.lookup(1) * self.lookup(2)
                self.info(
                    f"    -> ADD program[{self.direct(3)}] = {self.lookup(1)} * {self.lookup(2)} = {self.lookup(1) * self.lookup(2)}"
                )
                self.pc += 4
            elif instruction == OP.SAVE:
                if len(self.inputs) == 0:
                    # print("Not enough input!")
                    self.state = "waiting_input"
                    break
                this_input = self.inputs.pop(0)

                self.memory[self.lookup_left(1)] = this_input

                self.info(
                    f"    -> SAVE program[{self.lookup(1)}] = INPUT = {this_input}"
                )
                self.pc += 2
            elif instruction == OP.WRITE:
                self.outputs.append(self.lookup(1))
                self.info(f"    -> WRITE {self.lookup(1)} = OUTPUT")
                self.pc += 2
            elif instruction == OP.JUMP_IF_TRUE:
                if self.lookup(1) != 0:
                    self.info(
                        f"    -> JUMP_IF_TRUE [{self.lookup(1)}] != 0, setting i = [{self.lookup(2)}]"
                    )
                    self.pc = self.lookup(2)
                else:
                    self.info(
                        f"    -> JUMP_IF_TRUE [{self.lookup(1)}] == 0, doing normal i+= 3"
                    )
                    self.pc += 3
            elif instruction == OP.JUMP_IF_FALSE:
                if self.lookup(1) == 0:
                    self.info(
                        f"    -> JUMP_IF_FALSE [{self.lookup(1)}] == 0, setting i = [{self.lookup(2)}]"
                    )
                    self.pc = self.lookup(2)
                else:
                    self.info(
                        f"    -> JUMP_IF_FALSE [{self.lookup(1)}] != 0, doing normal i+= 3"
                    )
                    self.pc += 3
            elif instruction == OP.LESS_THAN:
                if self.lookup(1) < self.lookup(2):
                    self.info(
                        f"    -> LESS_THAN [{self.lookup(1)}] < [{self.lookup(2)}], setting program[{self.lookup_left(3)}] = 1"
                    )
                    self.memory[self.lookup_left(3)] = 1
                else:
                    self.info(
                        f"    -> LESS_THAN [{self.lookup(1)}] not < [{self.lookup(2)}], setting program[{self.lookup_left(3)}] = 0"
                    )
                    self.memory[self.lookup_left(3)] = 0
                self.pc += 4
            elif instruction == OP.EQUALS:
                if self.lookup(1) == self.lookup(2):
                    self.info(
                        f"    -> EQUALS [{self.lookup(1)}] == [{self.lookup(2)}], setting program[{self.lookup_left(3)}] = 1"
                    )
                    self.memory[self.lookup_left(3)] = 1
                else:
                    self.info(
                        f"    -> EQUALS [{self.lookup(1)}] != [{self.lookup(2)}], setting program[{self.lookup_left(3)}] = 0"
                    )
                    self.memory[self.lookup_left(3)] = 0
                self.pc += 4
            elif instruction == OP.SET_REL_BASE:
                adj = self.lookup(1)
                self.relative_base += adj
                self.info(
                    f"    -> ADJUST RELATIVE BASE by [{adj}]. NEW BASE = [{self.relative_base}]"
                )
                self.pc += 2
            elif instruction == OP.STOP:
                self.state = "halted"
                break


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


def solve1(program_in, inputs):
    """ Given a program and inputs, make a new VM, run the program, and return
    its outputs when it stops. """
    c = Computer(program_in, inputs)
    c.execute()
    return c.outputs


def amplify_once_find_max_seq(program_in):
    """Try every combination of phase settings on the amplifiers. What is the
    highest signal that can be sent to the thrusters? (Max Val)"""
    max_val = 0
    max_sequence = []

    for seq in permutations([0, 1, 2, 3, 4]):
        phase_sequence = list(seq)
        val = amplify_once(program_in, phase_sequence)
        if val > max_val:
            max_val = val
            max_sequence = phase_sequence
    return [max_val, max_sequence]


def amplify_once(program_in, phase_sequence):
    input_signal = 0
    for setting in phase_sequence:
        outputs = solve1(program_in, [setting, input_signal])
        input_signal = outputs[0]
    return input_signal


def amplify_loop(program_in, phase_sequence):
    cpus = []
    for i in range(5):
        cpus.append(Computer(program_in, [phase_sequence[i]]))

    i = 0
    next_input = 0
    while True:
        cpus[i].add_input(next_input)
        cpus[i].execute()
        if cpus[i].state == "halted" and i == 4:
            # print("halted")
            return cpus[i].outputs[0]
        next_input = cpus[i].pop_output()
        i = (i + 1) % 5


def amplify_loop_max_seq(program_in):
    max_val = 0
    max_sequence = []
    for seq in permutations([5, 6, 7, 8, 9]):
        phase_sequence = list(seq)
        val = amplify_loop(program_in, phase_sequence)
        if val > max_val:
            max_val = val
            max_sequence = phase_sequence
    return [max_val, max_sequence]


COMPLEX_OF_DIR = {
    "U": complex(0, -1),
    "R": complex(1, 0),
    "D": complex(0, 1),
    "L": complex(-1, 0),
}


def turn_right(direction):
    return turn(direction, 1)


def turn_left(direction):
    return turn(direction, -1)


def turn(direction, n):
    directions = list(COMPLEX_OF_DIR.keys())
    new_index = (directions.index(direction) + n) % len(directions)
    return directions[new_index]


class PainterRobot(object):
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])
        self.grid = defaultdict(lambda: 0)

    def input(self, val):
        self.cpu.add_input(val)

    def add_quarters(self):
        self.cpu.memory[0] = 2

    def run_and_return_grid(self):
        cpu = self.cpu
        self.cpu.memory[0] = 2
        grid = self.grid

        cpu.execute()
        while cpu.has_output():
            x = cpu.pop_output()
            y = cpu.pop_output()
            what = cpu.pop_output()
            grid[complex(x, y)] = what

        return grid

    def part2(self):
        return 5


def get_move(grid):
    ball = list(grid.keys())[list(grid.values()).index(4)]
    ball_x = int(ball.real)
    paddle = list(grid.keys())[list(grid.values()).index(3)]
    paddle_x = int(paddle.real)
    if ball_x > paddle_x:
        return "r"
    if ball_x < paddle_x:
        return "l"
    return "n"


def part1(program_in):
    robot = PainterRobot(program_in)
    grid = robot.run_and_return_grid()
    robot.add_quarters()
    display(grid)
    while True:
        a = get_move(grid)
        # a = input()
        if a == "l":
            robot.input(-1)
        elif a == "r":
            robot.input(1)
        else:
            robot.input(0)
        grid = robot.run_and_return_grid()
        display(grid)

    # print(grid)
    # print(list(grid.values()).count(2))
    return len(list(grid.keys()))


def display(grid):
    system("clear")
    for y in range(25):
        for x in range(45):
            char = grid[complex(x, y)]
            print_char = " "
            if char == 1:
                print_char = "W"
            elif char == 2:
                print_char = "B"
            elif char == 3:
                print_char = "="
            elif char == 4:
                print_char = "*"
            print(print_char, end="")
        print("")
    print(f"Score {grid[complex(-1, 0)]}")


def part2(program_in):
    robot = PainterRobot(program_in)
    grid = robot.run_and_return_grid()
    for y in range(-3, 7):
        for x in range(-5, 45):
            value = grid[complex(x, y)]
            if value == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print("")
    return "Look above ^"


if __name__ == "__main__":
    system("clear")
    a = input()
    program = parse("../../13/input.txt")
    print(part1(program))
    # print("Part 2:")
    # print(part2(program))
