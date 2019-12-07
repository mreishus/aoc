#!/usr/bin/env python

from itertools import permutations
import time

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
    STOP = 99


class MODE:
    POSITION = 0
    IMMEDIATE = 1


def digit_from_right(x, n):
    return x // (10 ** n) % 10


class Computer(object):
    def __init__(self, memory, inputs):
        self.memory = memory.copy()
        self.inputs = inputs.copy()
        self.outputs = []
        self.pc = 0
        self.state = "new"

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
        raise Exception("Unknown mode")

    def info(self, string):
        if DEBUG:
            print(string)

    def add_input(self, x):
        self.inputs.append(x)

    def pop_output(self):
        return self.outputs.pop(0)

    def execute(self):
        if self.state == "halted":
            print("Refusing to execute; is halted")
        self.state = "running"
        while True:
            instruction = self.memory[self.pc] % 100
            if instruction == OP.ADD:
                self.memory[self.direct(3)] = self.lookup(1) + self.lookup(2)
                self.info(
                    f"    -> ADD program[{self.direct(3)}] = {self.lookup(1)} + {self.lookup(2)} = {self.lookup(1) + self.lookup(2)}"
                )
                self.pc += 4
            elif instruction == OP.MULT:
                self.memory[self.direct(3)] = self.lookup(1) * self.lookup(2)
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
                self.memory[self.direct(1)] = this_input
                self.info(
                    f"    -> SAVE program[{self.direct(1)}] = INPUT = {this_input}"
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
                        f"    -> LESS_THAN [{self.lookup(1)}] < [{self.lookup(2)}], setting program[{self.direct(3)}] = 1"
                    )
                    self.memory[self.direct(3)] = 1
                else:
                    self.info(
                        f"    -> LESS_THAN [{self.lookup(1)}] not < [{self.lookup(2)}], setting program[{self.direct(3)}] = 0"
                    )
                    self.memory[self.direct(3)] = 0
                self.pc += 4
            elif instruction == OP.EQUALS:
                if self.lookup(1) == self.lookup(2):
                    self.info(
                        f"    -> EQUALS [{self.lookup(1)}] == [{self.lookup(2)}], setting program[{self.direct(3)}] = 1"
                    )
                    self.memory[self.direct(3)] = 1
                else:
                    self.info(
                        f"    -> EQUALS [{self.lookup(1)}] != [{self.lookup(2)}], setting program[{self.direct(3)}] = 0"
                    )
                    self.memory[self.direct(3)] = 0
                self.pc += 4
            elif instruction == OP.STOP:
                self.state = "halted"
                break


def parse(filename):
    return [int(num) for num in open(filename).readline().strip().split(",")]


def solve1(program_in, inputs):
    c = Computer(program_in, inputs)
    c.execute()
    return c.outputs


def part1(program_in):
    max_val = 0
    max_sequence = []

    for seq in permutations([0, 1, 2, 3, 4]):
        phase_sequence = list(seq)
        val = part1_onetry(program_in, phase_sequence)
        if val > max_val:
            max_val = val
            max_sequence = phase_sequence
    return [max_val, max_sequence]


def part1_onetry(program_in, phase_sequence):
    input_signal = 0
    for setting in phase_sequence:
        outputs = solve1(program_in, [setting, input_signal])
        input_signal = outputs[0]
    return input_signal


def part2_onetry(program_in, phase_sequence):
    cpus = []
    # print(program_in)
    # print(phase_sequence)
    for i in range(5):
        cpus.append(Computer(program_in, [phase_sequence[i]]))

    i = 0
    next_input = 0
    while True:
        # print(i)
        cpus[i].add_input(next_input)
        cpus[i].execute()
        if cpus[i].state == "halted" and i == 4:
            # print("halted")
            # print(cpus[i].outputs[0])
            return cpus[i].outputs[0]
        next_input = cpus[i].pop_output()
        # print(f"Got output {next_input} from computer {i}")
        i = (i + 1) % 5
    # print("STate")
    # print(cpus[0].state)
    # print("Outpuits")
    # print(cpus[0].outputs)


def part2(program_in):
    max_val = 0
    max_sequence = []
    for seq in permutations([5, 6, 7, 8, 9]):
        phase_sequence = list(seq)
        val = part2_onetry(program_in, phase_sequence)
        if val > max_val:
            max_val = val
            max_sequence = phase_sequence
    return [max_val, max_sequence]


if __name__ == "__main__":
    file_data = parse("../input.txt")
    print("Part1: ")
    # test_prog = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    # # You guessed 20314
    [max_val, max_seq] = part1(file_data)
    print("Max val:")
    print(max_val)
    print("Max seq:")
    print(max_seq)
    print("--")
    test_prog = [
        3,
        26,
        1001,
        26,
        -4,
        26,
        3,
        27,
        1002,
        27,
        2,
        27,
        1,
        27,
        26,
        27,
        4,
        27,
        1001,
        28,
        -1,
        28,
        1005,
        28,
        6,
        99,
        0,
        0,
        5,
    ]
    # z = part2_onetry(test_prog, [9, 8, 7, 6, 5])
    # print(z)

    test_prog2 = [
        3,
        52,
        1001,
        52,
        -5,
        52,
        3,
        53,
        1,
        52,
        56,
        54,
        1007,
        54,
        5,
        55,
        1005,
        55,
        26,
        1001,
        54,
        -5,
        54,
        1105,
        1,
        12,
        1,
        53,
        54,
        53,
        1008,
        54,
        0,
        55,
        1001,
        55,
        1,
        55,
        2,
        53,
        55,
        53,
        4,
        53,
        1001,
        56,
        -1,
        56,
        1005,
        56,
        6,
        99,
        0,
        0,
        0,
        0,
        10,
    ]
    # z = part2_onetry(test_prog2, [9, 7, 8, 5, 6])
    # print(z)

    # zz = part2(test_prog)
    # print(zz)
    # zz = part2(test_prog2)
    # print(zz)
    print("Part 2")
    zz = part2(file_data)
    print(zz)
    # [max_val, max_seq] = part2(test_prog)
    # print("Max val:")
    # print(max_val)
    # print("Max seq:")
    # print(max_seq)
