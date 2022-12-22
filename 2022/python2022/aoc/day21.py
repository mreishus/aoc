#!/usr/bin/env python
"""
Advent Of Code 2022 Day 21
https://adventofcode.com/2022/day/3
"""
from typing import List
import re
from functools import cache
import random

PARSER = re.compile(r"(\w{4}) (\S) (\w{4})")


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    label, equation = line.split(": ")
    is_constant = False
    if re.search(PARSER, equation):
        (x, y, z) = re.search(PARSER, equation).groups()
        equation = (x, y, z)
    else:
        equation = int(equation)
        is_constant = True
    return (label, equation, is_constant)


@cache
def get_value(data, label_in):
    for (label, equation, is_constant) in data:
        if label != label_in:
            continue
        if is_constant:
            return equation
        else:
            (x, y, z) = equation
            x = get_value(data, x)
            z = get_value(data, z)
            if y == "+":
                return x + z
            elif y == "*":
                return x * z
            elif y == "-":
                return x - z
            elif y == "/":
                return x // z


def get_value2(data, label_in, num):
    if label_in == "humn":
        return num
    for (label, equation, is_constant) in data:
        if label != label_in:
            continue
        if is_constant:
            return equation
        elif label == "root":
            (x, y, z) = equation
            x = get_value2(data, x, num)
            z = get_value2(data, z, num)
            print(num, "ROOT ", x, z, x == z, x // 1000000000, z // 1000000000, z - x)
            if x == z:
                print("FOUND")
                print("FOUND")
                print("FOUND")
                print("FOUND")
                print(num)
                print("FOUND")
                print("FOUND")
                print("FOUND")
                print("FOUND")
                exit()

        else:
            (x, y, z) = equation
            x = get_value2(data, x, num)
            z = get_value2(data, z, num)
            if y == "+":
                return x + z
            elif y == "*":
                return x * z
            elif y == "-":
                return x - z
            elif y == "/":
                return x // z


def p1(data):
    data = tuple(data)
    return get_value(data, "root")


def p2(data, num):
    data = tuple(data)
    return get_value2(data, "root", num)


class Day21:
    """AoC 2022 Day 21"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        data = tuple(data)
        print(data)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        data = tuple(data)
        # for i in range(15):
        #     j = 10**i + random.randint(0, 10**i)
        #     p2(data, j)
        start = 3423156653201
        start = 3423276653201
        start = 3423279853201
        start = 3423279931201
        start = 3423279932861
        while True:
            # num = int(input())
            # print("")
            start += 1
            num = start
            print(num)
            p2(data, num)
            # print(p2(data, num))
        return -2
