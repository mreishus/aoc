#!/usr/bin/env python
"""
Advent Of Code 2020 Day 25
https://adventofcode.com/2020/day/25
"""

from typing import List


def parse(filename: str):
    with open(filename) as file:
        return [int(line.strip()) for line in file.readlines()]


def p1(keys: List[int]):
    # card -> Transform(7, card_loop_size) = Card Pub Key
    # door -> Transform*7, door_loop_size) = Door pub key
    # They exchange pubkeys
    # card -> transform(door_pub_key, card_loop_size) = Encryption Key
    # door -> Transform(card_pub_key, door_loop_size) = Same Encryption Key

    card_loop_size = get_loop_size(keys[0])
    return transform(keys[1], card_loop_size)
    # Alternative:
    # door_loop_size = get_loop_size(keys[1])
    # print(transform(keys[0], door_loop_size))


def get_loop_size(pub_key):
    val = 1
    subj_num = 7

    for i in range(1, 1_000_000_000):
        val *= subj_num
        val = val % 20201227

        if val == pub_key:
            return i

    return None


def transform(subj_num, loop_size):
    val = 1
    for _ in range(loop_size):
        val *= subj_num
        val = val % 20201227
    return val


class Day25:
    """ AoC 2020 Day 25 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 25 part 1 """
        data = parse(filename)
        return p1(data)
