#!/usr/bin/env python
"""
Advent Of Code 2020 Day 12
https://adventofcode.com/2020/day/12
"""


def parse(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
        start_time = int(lines[0])
        nums = lines[1].split(",")
        for i, num in enumerate(nums):
            if num != "x":
                nums[i] = int(num)
        return start_time, nums


def p1(data):
    start_time, nums = data
    nums = [int(num) for num in nums if num != "x"]

    depart_time = None
    depart_bus = None

    start_time = int(start_time)
    for t in range(start_time, start_time + 100):
        for n in nums:
            # print(t, n, t % n)
            if t % n == 0:
                depart_time = t
                depart_bus = n
                break
        if depart_time is not None:
            break

    wait_time = depart_time - start_time
    return wait_time * depart_bus


def p2(data):
    _start_time, nums = data

    # nums = [17, "x", 13, 19]
    # nums = [67, 7, "x", 59, 61]

    def test_time(t):
        for i, n in enumerate(nums):
            if n == "x":
                continue
            if (t + i) % n == 0:
                continue
            return False, i
        return True, 0

    def partial_product(broken_where):
        consider = [num for num in nums[0:broken_where] if num != "x"]
        prod = 1
        for c in consider:
            prod *= c
        return prod

    x = 0
    while True:
        worked, broken_where = test_time(x)
        if worked:
            return x
        # print(f"{x} {broken_where} | {nums}")
        x += partial_product(broken_where)
        # rem = x % nums[0]
        # if rem > 0:
        #     x += nums[0] - rem


class Day13:
    """ AoC 2020 Day 12 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 13 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 13 part 2 """
        data = parse(filename)
        return p2(data)
