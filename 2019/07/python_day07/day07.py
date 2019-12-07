#!/usr/bin/env python

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

    def execute(self):
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
    for a in range(5):
        for b in range(5):
            if b == a:
                continue
            for c in range(5):
                if c == b or c == a:
                    continue
                for d in range(5):
                    if d == c or d == b or d == a:
                        continue
                    for e in range(5):
                        if e == d or e == c or e == b or e == a:
                            continue
                        phase_sequence = [a, b, c, d, e]
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


if __name__ == "__main__":
    file_data = parse("../input.txt")
    print("Part1: ")
    test_prog = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    # You guessed 20314
    [max_val, max_seq] = part1(file_data)
    print("Max val:")
    print(max_val)
    print("Max seq:")
    print(max_seq)
    # print(part1(test_prog, [4, 3, 2, 1, 0]))
    # print(solve1(file_data, [3, 0]))
    # print("Part2: ")
    # print(solve1(file_data, [5]))
