#!/usr/bin/env python
"""
Advent Of Code 2022 Day 11
https://adventofcode.com/2022/day/11
"""
import re
import math


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip()
        blocks = lines.split("\n\n")
        return [parse_block(block) for block in blocks]


def parse_block(block: str):
    lines = block.splitlines()
    num = ints(lines[0])[0]
    items = ints(lines[1])

    do_square = False
    add = 0
    mult = 1
    if re.search(r"\* old", lines[2]):
        do_square = True
    elif re.search(r"\+ (\d+)", lines[2]):
        add = ints(lines[2])[0]
    elif re.search(r"\* (\d+)", lines[2]):
        mult = ints(lines[2])[0]

    test_div = ints(lines[3])[0]
    if_true = ints(lines[4])[0]
    if_false = ints(lines[5])[0]
    return {
        "num": num,
        "items": items,
        "test_div": test_div,
        "if_true": if_true,
        "if_false": if_false,
        "add": add,
        "mult": mult,
        "do_square": do_square,
        "inspects": 0,
    }


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def tick(data, is_part2=False, this_lcm=1):
    for i in range(len(data)):
        while len(data[i]["items"]) > 0:
            worry = data[i]["items"].pop(0)
            data[i]["inspects"] += 1
            if data[i]["do_square"]:
                worry = worry * worry
            worry += data[i]["add"]
            worry *= data[i]["mult"]

            if not is_part2:
                worry //= 3
            else:
                worry %= this_lcm

            remainder = worry % data[i]["test_div"]
            target = None
            if remainder == 0:
                target = data[i]["if_true"]
            else:
                target = data[i]["if_false"]

            data[target]["items"].append(worry)

    # print("round done")
    # for i in range(len(data)):
    #     print(f"i: {i} {data[i]['items']} {data[i]['inspects']}")
    return data


def mult_top_two_inspects(data):
    total_inspects = []
    for i in range(len(data)):
        total_inspects.append(data[i]["inspects"])
    total_inspects.sort()
    top_2 = total_inspects[-2:]
    return top_2[0] * top_2[1]


class Day11:
    """AoC 2022 Day 11"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        for _ in range(20):
            data = tick(data, is_part2=False)
        return mult_top_two_inspects(data)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)

        this_lcm = 1
        for i in range(len(data)):
            this_lcm = lcm(this_lcm, data[i]["test_div"])

        for _ in range(10000):
            data = tick(data, is_part2=True, this_lcm=this_lcm)
        return mult_top_two_inspects(data)
