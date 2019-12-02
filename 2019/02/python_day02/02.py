#!/usr/bin/env python
import math


class OP:
    ADD = 1
    MULT = 2
    STOP = 99


def compute(program):
    i = 0
    while True:
        instruction = program[i]
        if instruction == OP.ADD:
            pos_in1 = program[i + 1]
            pos_in2 = program[i + 2]
            pos_out = program[i + 3]
            program[pos_out] = program[pos_in1] + program[pos_in2]
            i += 4
        elif instruction == OP.MULT:
            pos_in1 = program[i + 1]
            pos_in2 = program[i + 2]
            pos_out = program[i + 3]
            program[pos_out] = program[pos_in1] * program[pos_in2]
            i += 4
        elif instruction == OP.STOP:
            break
        else:
            raise ValueError(f"compute: Found unknown instruction {instruction}")
    return program


def parse(filename):
    return [int(num) for num in open(filename).readline().strip().split(",")]


def part1(program_in):
    p = program_in.copy()
    p[1] = 12
    p[2] = 2
    p = compute(p)
    return p[0]


def part2_eval(program_in, noun, verb):
    p = program_in.copy()
    p[1] = noun
    p[2] = verb
    p = compute(p)
    return p[0]


def part2_answer(noun, verb):
    return 100 * noun + verb


def part2_brute(program_in):
    """ Solve Part2 using brute force. """
    p = program_in.copy()
    for noun in range(101):
        for verb in range(101):
            if part2_eval(p, noun, verb) == 19_690_720:
                print(f"noun: {noun} verb: {verb}")
                return part2_answer(noun, verb)
    raise ValueError("part2_brute: Couldn't find an answer")


def p2clamp(n):
    return clamp(n, 0, 100)


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def loss(program, noun, verb):
    want = 19_690_720
    got = part2_eval(program, noun, verb)
    return abs(want - got)


def testme(x):
    return 1 if x > 0 else -1


def part2_descent(program_in):
    """ Solve Part2 using gradient descent. """
    p = program_in.copy()
    noun = 50
    verb = 50
    for i in range(500):
        l = loss(p, noun, verb)
        if l == 0:
            return part2_answer(noun, verb)
        lx_left = loss(p, p2clamp(noun - 1), verb)
        if lx_left == 0:
            return part2_answer(noun - 1, verb)
        lx_right = loss(p, p2clamp(noun + 1), verb)
        if lx_right == 0:
            return part2_answer(noun + 1, verb)
        x_diff = (lx_right - lx_left) / 2
        x_steps = 0
        if x_diff != 0:
            x_steps = l / x_diff * -1

        ly_up = loss(p, noun, p2clamp(verb + 1))
        if ly_up == 0:
            return part2_answer(noun, verb + 1)
        ly_down = loss(p, noun, p2clamp(verb - 1))
        if ly_down == 0:
            return part2_answer(noun, verb - 1)
        y_diff = (ly_up - ly_down) / 2
        y_steps = 0
        if y_diff != 0:
            y_steps = l / y_diff * -1

        # print("--")
        print(f"i: #{i} x: #{noun} y: #{verb}")
        # print(f"loss: {l} lossx_left: {lx_left} lossx_right {lx_right}")
        # print(f"lossy_up: {ly_up} lossy_down: {ly_down}")
        # print(f"x_diff: {x_diff} y_diff: {y_diff}")
        # print(f"x_steps: {x_steps} y_steps: {y_steps}")
        if abs(x_steps) <= 1000:
            noun = p2clamp(noun + round_away0(x_steps * 0.25))
        if abs(y_steps) <= 1000:
            verb = p2clamp(verb + round_away0(y_steps * 0.25))


def round_away0(value):
    return math.ceil(value) if value >= 0 else math.floor(value)


program = parse("../input.txt")
# program = parse("../D2P2-RealisticBigBoy")
# program = parse("../D2P2-VeryBigBoy")
print("part 1:")
print(part1(program))
print("part 2 (brute):")
print(part2_brute(program))
print("part 2 (gradient descent):")
print(part2_descent(program))
