#!/usr/bin/env python

import itertools
from collections import deque


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
        # Skip N + 1 | Combine with slicing "for digits in digits[output:i]" to skip
        # half the triangle
        seq = itertools.islice(sequence(output_i + 1), 1 + output_i, None)

        this_digit = 0
        for digit in itertools.islice(digits, output_i, None):
            this_digit += next(seq) * digit
        this_digit = abs(this_digit) % 10
        result.append(this_digit)
    return result


def multiple_transform(digits, n):
    for i in range(n):
        digits = transform(digits)
    return digits


def transform_secondhalf(digits):
    result = deque()
    num = 0
    for i in range(len(digits)):
        num = (num + digits.pop()) % 10
        result.appendleft(num)
    return result


def part1_secondhalf(digits):
    start_slice = len(digits) // 2
    second_half = digits[start_slice:]
    second_half = deque(second_half)

    for i in range(100):
        second_half = transform_secondhalf(second_half)
    print(second_half)


def part1(digits):
    result = multiple_transform(digits, 100)
    return "".join(str(x) for x in result[:8])


def part2(digits):
    # Message offset = first 7 digits converted to a number
    message_offset = int("".join(str(x) for x in digits[:7]))
    print(f"Computing part 2 with message offset {message_offset}...")

    # digits *= 10_000
    second_half = deque(digits * 5000)
    print("Starting to iterate")
    for i in range(100):
        second_half = transform_secondhalf(second_half)

    result = list(second_half)
    skip = message_offset - (len(digits) * 5000)
    # print(f"Skip [{skip}]")
    # print(f"Result length [{len(result)}]")
    answer = result[skip : 8 + skip]
    print(f"Found answer {answer} ...")
    return int("".join(str(x) for x in answer))


if __name__ == "__main__":
    digits = parse16("../../16/input.txt")

    print("Part 1:")
    print(part1(digits))
    print("Part 2:")
    print(part2(digits))
