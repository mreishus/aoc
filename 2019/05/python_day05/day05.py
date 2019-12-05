#!/usr/bin/env python
from collections import Counter
import re

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


def compute(program, input_value):
    i = 0
    mode = MODE.POSITION
    output_value = -99
    while True:
        raw_instruction = program[i]
        (mode3, mode2, mode1, instruction) = decode(raw_instruction)
        if DEBUG:
            print("")
            if i % 4 == 0:
                print(data)
            if i + 2 < len(data):
                print(
                    f"i[{i}] inst[{instruction}] next1[{ program[i+1] }] next1[{ program[i+2] }]  mode1[{mode1}] mode2[{mode2}]  "
                )
            else:
                print(f"i[{i}] inst[{instruction}] mode1[{mode1}] mode2[{mode2}] ")

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

            if DEBUG:
                print(
                    f"    -> ADD program[{pos_out}] = {add1} + {add2} = {add1 + add2}"
                )
            program[pos_out] = add1 + add2
            if i != pos_out:
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

            if DEBUG:
                print(
                    f"    -> MULT program[{pos_out}] = {mult1} * {mult2} = {mult1 * mult2}"
                )
            program[pos_out] = mult1 * mult2
            if i != pos_out:
                i += 4
        elif instruction == OP.SAVE:
            some_input = input_value  # 4  # 99  # XXX TODO
            pos_out = program[i + 1]
            program[pos_out] = some_input
            if DEBUG:
                print(f"    -> SAVE program[{pos_out}] = INPUT = {some_input}")
            if i != pos_out:
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
            print(f"output: [{some_output}]")
            output_value = some_output
            i += 2
        elif instruction == OP.JUMP_IF_TRUE:
            pos_in1 = program[i + 1]
            pos_in2 = program[i + 2]

            p1 = 0
            if mode1 == MODE.POSITION:
                p1 = program[pos_in1]
            elif mode1 == MODE.IMMEDIATE:
                p1 = pos_in1
            else:
                raise Exception("jump if truee: unknown p1")

            p2 = 0
            if mode2 == MODE.POSITION:
                p2 = program[pos_in2]
            elif mode2 == MODE.IMMEDIATE:
                p2 = pos_in2
            else:
                raise Exception("jump if truee: unknown p2")

            if p1 != 0:
                if DEBUG:
                    print(f"    -> JUMP_IF_TRUE [{p1}] != 0, setting i = [{p2}]")
                i = p2
            else:
                if DEBUG:
                    print(f"    -> JUMP_IF_TRUE [{p1}] == 0, doing normal i+= 3")
                i += 3

        elif instruction == OP.JUMP_IF_FALSE:
            pos_in1 = program[i + 1]
            pos_in2 = program[i + 2]

            p1 = 0
            if mode1 == MODE.POSITION:
                p1 = program[pos_in1]
            elif mode1 == MODE.IMMEDIATE:
                p1 = pos_in1
            else:
                raise Exception("jump if false: unknown p1")

            p2 = 0
            if mode2 == MODE.POSITION:
                p2 = program[pos_in2]
            elif mode2 == MODE.IMMEDIATE:
                p2 = pos_in2
            else:
                raise Exception("jump if false: unknown p2")

            if p1 == 0:
                if DEBUG:
                    print(f"    -> JUMP_IF_FALSE [{p1}] == 0, setting i = [{p2}]")
                i = p2
            else:
                if DEBUG:
                    print(f"    -> JUMP_IF_FALSE [{p1}] != 0, doing normal i+= 3")
                i += 3
        elif instruction == OP.LESS_THAN:
            pos_in1 = program[i + 1]
            pos_in2 = program[i + 2]
            pos_out = program[i + 3]

            p1 = 0
            if mode1 == MODE.POSITION:
                p1 = program[pos_in1]
            elif mode1 == MODE.IMMEDIATE:
                p1 = pos_in1
            else:
                raise Exception("less than: unknown p1")

            p2 = 0
            if mode2 == MODE.POSITION:
                p2 = program[pos_in2]
            elif mode2 == MODE.IMMEDIATE:
                p2 = pos_in2
            else:
                raise Exception("less than: unknown p2")

            # p3, writing, never check mode

            if p1 < p2:
                if DEBUG:
                    print(
                        f"    -> LESS_THAN [{p1}] < [{p2}], setting program[{pos_out}] = 1"
                    )
                program[pos_out] = 1
            else:
                if DEBUG:
                    print(
                        f"    -> LESS_THAN [{p1}] not < [{p2}], setting program[{pos_out}] = -"
                    )
                program[pos_out] = 0

            if i != pos_out:
                i += 4
        elif instruction == OP.EQUALS:
            pos_in1 = program[i + 1]
            pos_in2 = program[i + 2]
            pos_out = program[i + 3]

            p1 = 0
            if mode1 == MODE.POSITION:
                p1 = program[pos_in1]
            elif mode1 == MODE.IMMEDIATE:
                p1 = pos_in1
            else:
                raise Exception("less than: unknown p1")

            p2 = 0
            if mode2 == MODE.POSITION:
                p2 = program[pos_in2]
            elif mode2 == MODE.IMMEDIATE:
                p2 = pos_in2
            else:
                raise Exception("less than: unknown p2")

            if p1 == p2:
                if DEBUG:
                    print(
                        f"    -> EQUAL [{p1}] == [{p2}], setting program[{pos_out}] = 1"
                    )
                program[pos_out] = 1
            else:
                if DEBUG:
                    print(
                        f"    -> EQUAL [{p1}] != [{p2}], setting program[{pos_out}] = 0"
                    )
                program[pos_out] = 0

            if i != pos_out:
                i += 4
        elif instruction == OP.STOP:
            break
        else:
            raise ValueError(f"compute: Found unknown instruction {instruction}")
    return output_value


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


def solve1(program_in, input_value):
    p = program_in.copy()
    p = compute(p, input_value)
    return p


def solve2(data):
    return data


if __name__ == "__main__":
    file_data = parse("../input.txt")
    print("Part1: ")
    print(solve1(file_data, 1))
    print("Part2: ")
    print(solve1(file_data, 5))
