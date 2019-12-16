#!/usr/bin/env python

## Note: Day 2 doesn't work yet

import itertools
from collections import deque

# import numpy as np

# np.set_printoptions(edgeitems=10)
# np.core.arrayprint._line_width = 180

# from aoc.computer import Computer
# from aoc.day15 import Day15


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
        # if output_i % 10 == 0:
        #     print(f"  {output_i}", end="")

        # Skip 1 - Old school
        # seq = sequence(output_i + 1)
        # next(seq)

        # Skip 1 - New
        # seq = itertools.islice(sequence(output_i + 1), 1, None)

        # Skip N + 1 | Combine with slicing "for digits in digits[output:i]" to skip
        # half the triangle
        seq = itertools.islice(sequence(output_i + 1), 1 + output_i, None)

        this_digit = 0
        # for digit in itertools.islice(digits, output_i, None):
        # for digit in digits[output_i:]:
        for i in range(output_i, len(digits)):
            # print(digit, end="")
            # this_digit += next(seq) * digit
            # a = next(seq)
            # # print(f"{a} * {digit}   +   ", end="")
            # print(f"{a} * {digit}   +   ")
            this_digit += next(seq) * digits[i]
            # print(f"            {this_digit}")
        # print(f" = {this_digit}")
        this_digit = abs(this_digit) % 10
        result.append(this_digit)
    return result


def multiple_transform(digits, n):
    for i in range(n):
        print(i)
        digits = transform(digits)
    return digits


def transform_secondhalf(digits):
    result = deque()
    num = 0
    for i in range(len(digits)):
        num = (num + digits.pop()) % 10
        result.appendleft(num)
    return result
    # result = deque()
    # num = 0
    # for i in range(len(digits) - 1, -1, -1):
    #     num = (num + digits[i]) % 10
    #     result.appendleft(num)
    # return result


def part1_secondhalf(digits):
    start_slice = len(digits) // 2
    second_half = digits[start_slice:]
    second_half = deque(second_half)

    for i in range(100):
        second_half = transform_secondhalf(second_half)
    print(second_half)


def part1(digits):
    result = multiple_transform(digits, 100)
    return result
    # print(result)
    # return "".join(str(x) for x in result[:8])


def part2(digits):
    # Message offset = first 7 digits converted to a number
    message_offset = int("".join(str(x) for x in digits[:7]))
    print(f"Computing part 2 with message offset {message_offset}...")

    # digits *= 10_000
    second_half = deque(digits * 5000)
    print("Starting to iterate")
    for i in range(100):
        # for i in range(3):
        print(f"Step {i}")
        second_half = transform_secondhalf(second_half)

    # result = multiple_transform(digits, 100)
    result = list(second_half)
    skip = message_offset - (len(digits) * 5000)
    print(f"Skip [{skip}]")
    print(f"Result length [{len(result)}]")
    answer = result[skip : 8 + skip]
    print(f"Found answer {answer} ...")
    return answer


if __name__ == "__main__":

    # digits = parse16("../../16/input_small.txt")
    # print(digits)
    # for i in range(4):
    #     print(digits)
    #     digits = transform(digits)
    # digits = parse16_string("80871224585914546619083218645595")

    print("---")
    digits = parse16("../../16/input.txt")

    print("P1 end: Look for 985635")
    # print(part1(digits))
    # print(part1_secondhalf(digits))
    print(part2(digits))

    # inn = parse16("../../16/input.txt")
    # digits = parse16_string("80871224585914546619083218645595")
    # print(multiple_transform(digits, 100))
    # print("Part 1:")

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
