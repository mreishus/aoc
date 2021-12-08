#!/usr/bin/env python
"""
Advent Of Code 2021 Day 08
https://adventofcode.com/2021/day/8
"""
from collections import defaultdict
import itertools


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    left, right = line.split(" | ")
    return (left.split(), right.split())


lookup = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}
by_len = {
    7: ["abcdefg"],
    6: ["abcdfg", "abcefg", "abdefg"],
    5: ["abdfg", "acdeg", "acdfg"],
    4: ["bcdf"],
    3: ["acf"],
    2: ["cf"],
}


def is_viable(answer, left):
    for thing in left:
        transformed = "".join(sorted([answer[x] for x in thing]))
        if transformed not in lookup:
            # print(f"{thing} -> {transformed}")
            # print("False!")
            return False
    # print("True!")
    return True


def deduce(left):
    possibilities = {
        "a": ["a", "b", "c", "d", "e", "f", "g"],
        "b": ["a", "b", "c", "d", "e", "f", "g"],
        "c": ["a", "b", "c", "d", "e", "f", "g"],
        "d": ["a", "b", "c", "d", "e", "f", "g"],
        "e": ["a", "b", "c", "d", "e", "f", "g"],
        "f": ["a", "b", "c", "d", "e", "f", "g"],
        "g": ["a", "b", "c", "d", "e", "f", "g"],
    }
    # print("")
    left = sorted(left, key=len)
    # print(left)
    last = ""
    for x in left:
        ## Very basic possibility removing
        candidates = by_len[len(x)]
        z = set("".join(candidates))
        for char in x:
            possibilities[char] = [
                letter for letter in possibilities[char] if letter in z
            ]

        ## Method: Look at new letters when size goes up
        if len(last) + 1 == len(x):
            new = [char for char in x if char not in last]
            ## "new" Are new characters in this mapping
            new_target = set("".join(by_len[len(x)])) - set("".join(by_len[len(last)]))
            if len(new_target) > 0:
                for char in new:
                    possibilities[char] = [
                        letter for letter in possibilities[char] if letter in new_target
                    ]

            # print(f"Found new: {new} | {new_target}")
            # print(possibilities)

        ## Clean up and look for possibilities with one value left
        remove_me = [v[0] for v in possibilities.values() if len(v) == 1]
        for char in possibilities.keys():
            if len(possibilities[char]) > 1:
                for to_remove in remove_me:
                    possibilities[char] = [
                        l for l in possibilities[char] if l not in to_remove
                    ]

        last = x
    # print("")
    # print(possibilities)

    ## Brute force
    v = list(possibilities.values())
    answer = {}
    for z in itertools.product(*v):
        ## Bad way of removing duplicate letters
        seen = defaultdict(int)
        consider = True
        for char in z:
            seen[char] += 1
            if seen[char] >= 2:
                consider = False
                break
        if not consider:
            continue

        ## Guar to not have duplicates
        ## Turn ('c', 'e', 'f' .. ) tuple into
        ## { 'a' => 'c', 'b' => 'e', 'c' => 'f', ... } dict

        answer = {}
        this_char = "a"
        for char in z:
            answer[this_char] = char
            this_char = chr(ord(this_char) + 1)
        if is_viable(answer, left):
            break
    return answer


class Day08:
    """ AoC 2021 Day 08 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 08 part 1 """
        data = parse(filename)

        count = 0
        for left, right in data:
            for thing in right:
                l = len(thing)
                if l in [2, 4, 3, 7]:
                    # print(f"{thing} {l}")
                    count += 1

        # if len(data) < 20:
        #     print(data)
        return count
        # return -1

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 08 part 2 """
        data = parse(filename)
        total = 0
        for left, right in data:
            assignments = deduce(left)
            output = 0
            for thing in right:
                transformed = "".join(sorted([assignments[x] for x in thing]))
                output *= 10
                output += lookup[transformed]
            total += output

        return total
