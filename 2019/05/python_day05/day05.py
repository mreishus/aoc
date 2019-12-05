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
        return self.memory[self.pc + n]

    def lookup(self, n):
        instruction = self.memory[self.pc]
        # If instruction is 105, and n=1, mode is the "1", or the 2nd digit
        # from right 0 indexed (3rd when counting naturally)
        mode = digit_from_right(instruction, n + 1)
        if mode == MODE.POSITION:
            return self.memory[self.direct(n)]
        elif mode == MODE.IMMEDIATE:
            return self.direct(n)
        else:
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
                # Opcode 3 takes a single integer as input and saves it to the
                # position given by its only parameter. For example, the
                # instruction 3,50 would take an input value and store it at
                # address 50.
                this_input = self.inputs.pop(0)
                self.memory[self.direct(1)] = this_input
                self.info(
                    f"    -> SAVE program[{self.direct(1)}] = INPUT = {this_input}"
                )
                self.pc += 2
            elif instruction == OP.WRITE:
                # Opcode 4 outputs the value of its only parameter. For
                # example, the instruction 4,50 would output the value at
                # address 50.
                self.outputs.append(self.lookup(1))
                self.info(f"    -> WRITE {self.lookup(1)} = OUTPUT")
                self.pc += 2
            elif instruction == OP.JUMP_IF_TRUE:
                # Opcode 5 is jump-if-true: if the first parameter is non-zero,
                # it sets the instruction pointer to the value from the second
                # parameter. Otherwise, it does nothing.
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
                # Opcode 6 is jump-if-false: if the first parameter is zero, it
                # sets the instruction pointer to the value from the second
                # parameter. Otherwise, it does nothing.
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
                # Opcode 7 is less than: if the first parameter is less than
                # the second parameter, it stores 1 in the position given by
                # the third parameter. Otherwise, it stores 0.
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
                # Opcode 8 is equals: if the first parameter is equal to the
                # second parameter, it stores 1 in the position given by the
                # third parameter. Otherwise, it stores 0.
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


if __name__ == "__main__":
    file_data = parse("../input.txt")
    print("Part1: ")
    print(solve1(file_data, [1]))
    print("Part2: ")
    print(solve1(file_data, [5]))
