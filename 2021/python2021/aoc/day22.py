#!/usr/bin/env python
"""
Advent Of Code 2021 Day 22
https://adventofcode.com/2021/day/22
"""
from typing import List
import re
from collections import defaultdict
import numpy as np

PARSER = re.compile(r"thing (\d+),(\d+), stuff")


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]
        # lines = file.read().strip()
        # first, *blocks = lines.split("\n\n")
        # return (first, blocks)


def parse_line(line):
    on = line.startswith("on")
    [x1, x2, y1, y2, z1, z2] = ints(line)
    return [on, x1, x2, y1, y2, z1, z2]
    # (d, amount) = line.split(" ")
    # return (d, int(amount))


def parse_line2(line):
    (x, y) = re.search(PARSER, line).groups()
    return (x, y)


def first_line(filename: str) -> str:
    """ Given a filename, returns the first line of a file. """
    with open(filename) as file:
        return file.readline().strip()


def all_lines(filename: str) -> List[str]:
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


class Range:
    def __init__(self, x1, x2, y1, y2, z1, z2, operation):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.operation = operation

    def is_overlap(self, other):
        print(f"Isoverlap {self} {other}")
        x_over = False
        y_over = False
        z_over = False
        if self.x1 <= other.x1 and other.x1 <= self.x2:
            x_over = True
        if other.x1 <= self.x1 and self.x1 <= other.x2:
            x_over = True
        if self.y1 <= other.y1 and other.y1 <= self.y2:
            y_over = True
        if other.y1 <= self.y1 and self.y1 <= other.y2:
            y_over = True
        if self.z1 <= other.z1 and other.z1 <= self.z2:
            z_over = True
        if other.z1 <= self.z1 and self.z1 <= other.z2:
            z_over = True
        return x_over and y_over and z_over

    def __repr__(self):
        return f"[{self.x1}..{self.x2}, {self.y1}..{self.y2}, {self.z1}..{self.z2}]"


class Day22:
    """ AoC 2021 Day 22 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 22 part 1 """
        data = parse(filename)
        A = np.zeros((101, 101, 101))

        def translate(x):
            return x + 50  # -50 -> 0, 0 -> 50, 50 -> 100

        def clamp_min(k):
            return max(translate(-50), translate(k))

        def clamp_max(k):
            return min(translate(50), translate(k))

        # data = [data[0], data[1]]
        for op, x1, x2, y1, y2, z1, z2 in data:
            [x1, y1, z1] = [clamp_min(k) for k in [x1, y1, z1]]
            [x2, y2, z2] = [clamp_max(k) for k in [x2, y2, z2]]
            A[x1 : x2 + 1, y1 : y2 + 1, z1 : z2 + 1] = op
        print(np.count_nonzero(A))
        # if len(data) < 20:
        #     print(data)
        return -1

    @staticmethod
    def part1b(filename: str) -> int:
        """ Given a filename, solve 2021 day 22 part 1 """
        data = parse(filename)

        def translate(x):
            return x + 50  # -50 -> 0, 0 -> 50, 50 -> 100

        def clamp_min(k):
            return max(translate(-50), translate(k))

        def clamp_max(k):
            return min(translate(50), translate(k))

        # data = [data[0], data[1]]
        ranges = []
        for operation, x1, x2, y1, y2, z1, z2 in data:
            r = Range(x1, x2, y1, y2, z1, z2, operation)
            ranges.append(r)

        first_range = ranges.pop()
        range_buckets = [[ranges[0]]]
        for r in ranges:
            found_match = False
            match_index = 0

            for i, bucket in enumerate(range_buckets):
                if any(r.is_overlap(this_range) for this_range in bucket):
                    found_match = True
                    match_index = i
                    print(f"Any passed")
                    break

            print(f"Considering foudn match {found_match}")
            if not found_match:
                print("Making new bucket")
                new_bucket = [r]
                range_buckets.append(new_bucket)
            else:
                print(f"Trying to add to bucket {match_index}")
                range_buckets[match_index].append(r)

        total = 0
        for bucket in range_buckets:
            print(bucket)
            total += Day22.solve_bucket(bucket)

        return total

    @staticmethod
    def solve_bucket(bucket) -> int:
        min_x = 99
        min_y = 99
        min_z = 99
        max_x = -99
        max_y = -99
        max_z = -99
        for r in bucket:
            min_x = min(min_x, r.x1)
            min_y = min(min_y, r.y1)
            min_z = min(min_z, r.z1)
            max_x = max(max_x, r.x2)
            max_y = max(max_y, r.y2)
            max_z = max(max_z, r.z2)

        size_x = abs(min_x) + max_x + 1
        size_y = abs(min_y) + max_y + 1
        size_z = abs(min_z) + max_z + 1
        x_offset = abs(min_x)
        y_offset = abs(min_y)
        z_offset = abs(min_z)
        print("")
        print(f"Allocating for bucket size: {len(bucket)}.")
        print(f"{min_x} {max_x} | {min_y} {max_y} | {min_z} {max_z}")
        print("")

        if len(bucket) == 1:
            r = bucket[0]
            if not r.operation:
                return 0
            return size_x * size_y * size_z

        A = np.zeros((size_x, size_y, size_z), dtype=bool)

        for r in bucket:
            # print(f"{x1} {x2} {y1} {y2} {z1} {z2}")
            [x1, x2] = [k + x_offset for k in [r.x1, r.x2]]
            [y1, y2] = [k + y_offset for k in [r.y1, r.y2]]
            [z1, z2] = [k + z_offset for k in [r.z1, r.z2]]
            # print(f"{x1} {x2} {y1} {y2} {z1} {z2}")
            A[x1 : x2 + 1, y1 : y2 + 1, z1 : z2 + 1] = r.operation
        # print(np.count_nonzero(A))
        return np.count_nonzero(A)

    @staticmethod
    def part2_failed(filename: str) -> int:
        """ Given a filename, solve 2021 day 22 part 2 """
        data = parse(filename)
        # A = np.zeros((101, 101, 101))

        min_x = 99
        min_y = 99
        min_z = 99
        max_x = -99
        max_y = -99
        max_z = -99
        for op, x1, x2, y1, y2, z1, z2 in data:
            min_x = min(min_x, x1)
            min_y = min(min_y, y1)
            min_z = min(min_z, z1)
            max_x = max(max_x, x2)
            max_y = max(max_y, y2)
            max_z = max(max_z, z2)

        print(f"{min_x} {max_x} {min_y} {max_y} {min_z} {max_z}")
        size_x = abs(min_x) + max_x + 1
        size_y = abs(min_y) + max_y + 1
        size_z = abs(min_z) + max_z + 1
        x_offset = abs(min_x)
        y_offset = abs(min_y)
        z_offset = abs(min_z)
        A = np.zeros((size_x, size_y, size_z), dtype=bool)

        # data = [data[0], data[1]]
        for op, x1, x2, y1, y2, z1, z2 in data:
            print(f"{x1} {x2} {y1} {y2} {z1} {z2}")
            [x1, x2] = [k + x_offset for k in [x1, x2]]
            [y1, y2] = [k + y_offset for k in [y1, y2]]
            [z1, z2] = [k + z_offset for k in [z1, z2]]
            print(f"{x1} {x2} {y1} {y2} {z1} {z2}")
            print("--")
            A[x1 : x2 + 1, y1 : y2 + 1, z1 : z2 + 1] = op
        print(np.count_nonzero(A))
