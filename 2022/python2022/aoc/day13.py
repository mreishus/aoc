#!/usr/bin/env python
"""
Advent Of Code 2022 Day 13
https://adventofcode.com/2022/day/3
"""
import json
from functools import cmp_to_key
from copy import deepcopy


def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip()
        blocks = lines.split("\n\n")
        return [parse_block(block) for block in blocks]


def parse_block(block: str):
    b1, b2 = block.split("\n")
    return json.loads(b1), json.loads(b2)


def compare(a, b):
    for i in range(len(a)):
        if i >= len(b):
            return False, None

        atype = type(a[i])
        btype = type(b[i])
        # print(f"Looking at {a[i]} and {b[i]}. {atype} vs {btype}")

        ## First pass: Upgrade singleton lists
        if atype == int and btype == list:
            a = deepcopy(a)
            a[i] = [a[i]]
            atype = type(a[i])
        elif atype == list and btype == int:
            b = deepcopy(b)
            b[i] = [b[i]]
            btype = type(b[i])

        if atype == int and btype == int:
            #  If the left integer is higher than the right integer,
            #  the inputs are not in the right order.
            if a[i] < b[i]:
                # print(f"Returning true because left int is smaller {a[i]} < {b[i]}")
                return True, True
            if a[i] > b[i]:
                # print(f"Returning false because left int is higher {a[i]} > {b[i]}")
                return False, None
        elif atype == list and btype == list:
            compare_result, compare_override = compare(a[i], b[i])
            if not compare_result:
                # print("Returning false because compare returned false")
                return False, None
            if compare_override:
                # print("Returning true because compare returned true")
                return True, True
        else:
            raise Exception(f"Unknown types {atype} {btype}")

    # We compared everything. We're either in a "left ran out" state or a
    # "everything is equal" state, which is somewhat indeterminate.
    return True, len(a) < len(b)


class Day13:
    """AoC 2022 Day 13"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        total = 0
        for i, (left, right) in enumerate(data, 1):
            in_order, _ = compare(left, right)
            if in_order:
                total += i
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        all_pairs = []
        for (left, right) in data:
            all_pairs.append(left)
            all_pairs.append(right)
        ## Add divider packets
        all_pairs.append([[2]])
        all_pairs.append([[6]])

        def cmp_items(a, b):
            compare_result, compare_override = compare(a, b)
            if compare_result and compare_override:
                return -1
            elif not compare_result:
                return 1
            else:
                return 0

        all_pairs.sort(key=cmp_to_key(cmp_items))
        total = 1
        for i, p in enumerate(all_pairs, 1):
            # print(p)
            if p == [[6]] or p == [[2]]:
                total *= i

        return total
