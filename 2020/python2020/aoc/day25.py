#!/usr/bin/env python
"""
Advent Of Code 2020 Day 25
https://adventofcode.com/2020/day/25
"""

import re
from dataclasses import dataclass
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        # lines = file.read().strip()
        # lines = file.read().strip()
        # p1, p2 = lines.split("\n\n")
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    return line
    # (items_str, contains_str) = re.match(r"^(.*)\(contains (.*)\)$", line).groups()
    # result = []

    # while len(line) > 0:
    #     a = re.match(r"(e|se|sw|w|nw|ne)", line)
    #     if not a:
    #         return result
    #     found = a.groups()[0]
    #     result.append(found)
    #     line = line[len(found) :]
    # return result


def p1(data):
    # M6 Input
    keys = [2069194, 16426071]

    # card -> Transform(7, card_loop_size) = Card Pub Key
    # door -> Transform*7, door_loop_size) = Door pub key
    # They exchange pubkeys
    # card -> transform(door_pub_key, card_loop_size) = Encryption Key
    # door -> Transform(card_pub_key, door_loop_size) = Same key??
    print(get_loop_size(5764801))  # 8
    print(get_loop_size(17807724))  # 11
    print(transform(17807724, 8))
    print(transform(5764801, 11))
    # Want to see: 14897079
    ######3
    keys = [2069194, 16426071]
    card_loop_size = get_loop_size(keys[0])
    print(transform(keys[1], card_loop_size))
    door_loop_size = get_loop_size(keys[1])
    print(transform(keys[0], door_loop_size))

    return -1


def get_loop_size(pub_key):
    for i in range(1_000_000):
        if transform(7, i) == pub_key:
            if i % 1000 == 0:
                print(i, end=" ")
            return i
    return None


def transform(subj_num, loop_size):
    val = 1
    for i in range(loop_size):
        val *= subj_num
        val = val % 20201227
    return val


def p2(data):
    return -2


class Day25:
    """ AoC 2020 Day 25 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 25 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 25 part 2 """
        data = parse(filename)
        return p2(data)
