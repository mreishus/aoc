#!/usr/bin/env python
"""
Advent Of Code 2023 Day 15
https://adventofcode.com/2023/day/15
"""
import re
from collections import namedtuple

Item = namedtuple("Item", ["label", "value"])


def parse(filename: str):
    with open(filename) as file:
        first_line = file.readline().strip()
        return first_line.split(",")


def do_hash(instruction, value):
    for char in instruction:
        value += ord(char)
        value *= 17
        value %= 256
    return value


class Box:
    def __init__(self, box_label):
        self.box_label = box_label
        self.contents = []

    def __repr__(self):
        return f"Box({self.box_label}, {self.contents})"

    def add_or_replace(self, label, value):
        for i, item in enumerate(self.contents):
            if item.label == label:
                new_item = Item(label, value)
                self.contents[i] = new_item
                return
        self.contents.append(Item(label, value))

    def remove_and_shift_left(self, label):
        for i, item in enumerate(self.contents):
            if item.label == label:
                del self.contents[i]
                return
        # Not found - do nothing.


class Day15:
    """AoC 2023 Day 15"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        total = 0
        for instruction in data:
            value = do_hash(instruction, 0)
            total += value
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        boxes = [Box(i) for i in range(256)]
        for instruction in data:
            m = re.search(r"(\w+)([-=])(\d+)?", instruction)
            if not m:
                continue

            label, operation, value = m.group(1), m.group(2), m.group(3)
            i = do_hash(label, 0)  # Which box to use.

            if operation == "=":
                boxes[i].add_or_replace(label, value)
            elif operation == "-":
                boxes[i].remove_and_shift_left(label)
            else:
                raise Exception("Unknown operation")

        total_power = 0
        for i, box in enumerate(boxes):
            # One plus the box number of the lens in question.
            a = i + 1
            for j, item in enumerate(box.contents):
                # One plus the box number of the lens in question.
                b = j + 1
                # The power of the lens in question.
                c = int(item.value)
                total_power += a * b * c
        return total_power
