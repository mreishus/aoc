#!/usr/bin/env python
"""
Advent Of Code 2023 Day 6
https://adventofcode.com/2023/day/6
"""
import re
from typing import List


def parse(filename: str):
    with open(filename) as file:
        lines = file.readlines()
        times = ints(lines[0])
        distances = ints(lines[1])

        return list(zip(times, distances))


def parse2(filename: str):
    with open(filename) as file:
        lines = file.readlines()
        time = int(lines[0].replace("Time:", "").replace(" ", ""))
        distance = int(lines[1].replace("Distance:", "").replace(" ", ""))
        return time, distance


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def travel_distance(hold_time, race_time):
    if hold_time >= race_time:
        return 0
    speed = hold_time
    remain_time = race_time - hold_time
    return speed * remain_time


def p1_num_ways(race_time, distance):
    true_begin = None
    true_end = None

    for hold_time in range(1, race_time):
        if travel_distance(hold_time, race_time) > distance:
            true_begin = hold_time
            true_end = race_time
            break

    if true_begin is None:
        return 0

    for hold_time in reversed(range(1, race_time)):
        if travel_distance(hold_time, race_time) > distance:
            true_end = hold_time
            break

    return true_end - true_begin + 1


class Day06:
    """AoC 2023 Day 06"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        ways = 1
        for time, distance in data:
            ways *= p1_num_ways(time, distance)
        return ways

    @staticmethod
    def part2(filename: str) -> int:
        time, distance = parse2(filename)
        return p1_num_ways(time, distance)
