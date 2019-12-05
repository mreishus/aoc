#!/usr/bin/env python
from collections import Counter
import re


class OP:
    ADD = 1
    MULT = 2
    SAVE = 3
    WRITE = 4
    STOP = 99


class MODE:
    POSITION = 0
    IMMEDIATE = 1


# b = 1234
# b // 100 = 12
#     - (b // 100) // 10 = 1
#       (b // 100) % 10  = 2
# b % 100 = 34  (could be 5, no leading 0)


def decode(opcode_over_1000):
    x = opcode_over_1000
    firstsecond = (x // 100) // 10
    first = firstsecond // 10
    second = firstsecond % 10
    three = (x // 100) % 10
    fourfive = x % 100
    return (first, second, three, fourfive)


def compute(program):
    i = 0
    mode = MODE.POSITION
    while True:
        raw_instruction = program[i]
        (mode3, mode2, mode1, instruction) = decode(raw_instruction)

        if instruction == OP.ADD:
            pos_in1 = program[i + 1]
            pos_in2 = program[i + 2]
            pos_out = program[i + 3]

            add1 = 0
            if mode1 == MODE.POSITION:
                add1 = program[pos_in1]
            elif mode1 == MODE.IMMEDIATE:
                add1 = pos_in1
            else:
                raise Exception("add: Unknown mode1")

            add2 = 0
            if mode2 == MODE.POSITION:
                add2 = program[pos_in2]
            elif mode2 == MODE.IMMEDIATE:
                add2 = pos_in2
            else:
                raise Exception("add: Unknown mode2")

            program[pos_out] = add1 + add2
            i += 4
        elif instruction == OP.MULT:
            pos_in1 = program[i + 1]
            pos_in2 = program[i + 2]
            pos_out = program[i + 3]

            mult1 = 0
            if mode1 == MODE.POSITION:
                mult1 = program[pos_in1]
            elif mode1 == MODE.IMMEDIATE:
                mult1 = pos_in1
            else:
                raise Exception("mult: Unknown mode1")

            mult2 = 0
            if mode2 == MODE.POSITION:
                mult2 = program[pos_in2]
            elif mode2 == MODE.IMMEDIATE:
                mult2 = pos_in2
            else:
                raise Exception("mult: Unknown mode2")

            program[pos_out] = mult1 * mult2
            i += 4
        elif instruction == OP.SAVE:
            some_input = 1  # 99  # XXX TODO
            pos_out = program[i + 1]
            program[pos_out] = some_input
            i += 2
        elif instruction == OP.WRITE:

            pos_in = program[i + 1]
            zzz = 0
            if mode1 == MODE.POSITION:
                zzz = program[pos_in]
            elif mode1 == MODE.IMMEDIATE:
                zzz = pos_in
            else:
                raise Exception("write: unknown mode1")

            some_output = zzz
            print(f"output: [{some_output}]\n")
            i += 2
        elif instruction == OP.STOP:
            break
        else:
            raise ValueError(f"compute: Found unknown instruction {instruction}")
    return program


def add_one(x):
    return x + 1


# filename -> [ wires ]
# wire example: [ ("U", 5), ("D", 40), ... ]
# def parse(filename):
#     return [parse_line(line) for line in open(filename).readlines()]
def parse(filename):
    return [int(num) for num in open(filename).readline().strip().split(",")]


# line = "person:guy age:33"
# (a, b) = re.match("person:(\w+) age:(\d+)", line).groups()

# string -> wire
# wire example: [ ("U", 5), ("D", 40), ... ]
def parse_line(line):
    return [parse_step(step) for step in line.strip().split(",")]


def solve1(program_in):
    p = program_in.copy()
    p = compute(p)
    return p


def solve2(data):
    return data


if __name__ == "__main__":
    data = parse("../input.txt")
    # data = parse("../input_small.txt")
    print("Part1: ")
    print(solve1(data))
    # print("Part2: ")
    # print(solve2(data))
