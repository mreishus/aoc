#!/usr/bin/env python
from aoc.day10 import knot_hash


def hexify(string):
    return bin(int(string, 16))[2:]


def part1(magic):
    count = 0
    for i in range(128):
        key = magic + "-" + str(i)
        list_of_strings_hash = [
            hexify(letter).zfill(4) for letter in list(knot_hash(key))
        ]
        for string in list_of_strings_hash:
            count += sum(1 for letter in list(string) if letter == "1")
    return count


if __name__ == "__main__":
    # 128 knot hashes
    # Each hash has 128 bits which correspond to grid squares
    magic = "hfdlxzhv"
    print("Part1: ")
    print(part1(magic))
