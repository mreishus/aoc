#!/usr/bin/env python

## Note: Day 2 doesn't work yet

import itertools

# from aoc.computer import Computer
from aoc.day15 import Day15


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


def parse16(filename):
    with open(filename) as f:
        return [int(num) for num in list(f.readline().strip())]


def parse16_string(string):
    return [int(num) for num in list(string.strip())]


def sequence(n):
    # 0, 1, 0, -1
    a = itertools.repeat(0, n)
    b = itertools.repeat(1, n)
    c = itertools.repeat(0, n)
    d = itertools.repeat(-1, n)
    return itertools.cycle(itertools.chain(a, b, c, d))


def transform(digits):
    result = []
    for output_i, _ in enumerate(digits):
        seq = sequence(output_i + 1)
        next(seq)
        this_digit = 0
        for digit in digits:
            # this_digit += next(seq) * digit
            a = next(seq)
            # # print(f"{a} * {digit}   +   ", end="")
            # print(f"{a} * {digit}   +   ")
            this_digit += a * digit
            # print(f"            {this_digit}")
        # print(f" = {this_digit}")
        this_digit = abs(this_digit) % 10
        result.append(this_digit)
    return result
    # seq = sequence(phase_num)
    # _ = next(seq)
    # for digit in phase_num:
    #     result.append(


def multiple_transform(digits, n):
    for i in range(n):
        digits = transform(digits)
    return digits


def part1():
    digits = parse16("../../16/input.txt")
    result = multiple_transform(digits, 100)
    return result[:8].join("")


def part2():
    digits = parse16("../../16/input.txt")

    # Message offset = first 7 digits converted to a number
    message_offset = int("".join(str(x) for x in digits[:7]))
    print(message_offset)
    digits *= 1000
    result = multiple_transform(digits, 100)
    skip = message_offset
    answer = result[skip : 8 + skip]
    print(answer)


if __name__ == "__main__":
    # print(part1())
    print(part2())
    # inn = parse16("../../16/input.txt")
    # digits = parse16("../../16/input_small.txt")
    # digits = parse16_string("80871224585914546619083218645595")
    # print(multiple_transform(digits, 100))
    # print("Part 1:")
    # print(digits)
    # for i in range(4):
    #     digits = transform(digits)
    # print(digits)

    # it1 = sequence(1)
    # it2 = sequence(2)
    # print("Seq 1")
    # for i in range(20):
    #     print(next(it1))
    # print("Seq 2")
    # for i in range(20):
    #     print(next(it2))

    # for phase in range(1, 10):
    #     print(f"Phase {phase}")
    # # print(Day15.part1(program))
