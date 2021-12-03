#!/usr/bin/env python
"""
Advent Of Code 2021 Day 03
https://adventofcode.com/2021/day/3
"""
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        return [(line.strip()) for line in file.readlines()]


class Day03:
    """ AoC 2021 Day 03 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 03 part 1 """
        data = parse(filename)
        if len(data) < 15:
            print(data)

        a = data[0]
        common = ""
        leastc = ""
        for i, z in enumerate(a):
            seen = defaultdict(int)
            for item in data:
                seen[item[i]] += 1

            if seen["0"] > seen["1"]:
                common += "0"
                leastc += "1"
            else:
                common += "1"
                leastc += "0"
        # print(common)
        gamma = int(common, 2)
        epi = int(leastc, 2)
        return gamma * epi

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 03 part 2 """
        data = parse(filename)
        o2 = Day03.part1(filename)

        a = data[0]
        candidates = set(range(len(data)))
        # print(candidates)

        lessc = None
        lesscfull = ""
        for i, z in enumerate(a):
            seen = defaultdict(int)
            for cand in candidates:
                seen[data[cand][i]] += 1

            if seen["0"] > seen["1"]:
                lessc = "1"
            else:
                lessc = "0"

            to_remove = []
            for cand in candidates:
                if data[cand][i] != lessc:
                    to_remove.append(cand)
            candidates -= set(to_remove)
            if len(candidates) == 1:
                lesscfull = data[list(candidates)[0]]
                break
            # print(candidates)
            # print("--")

        # if len(data) < 15:
        #     print(data)
        co2 = int(lesscfull, 2)

        lessc = None
        lesscfull = ""
        candidates = set(range(len(data)))
        for i, z in enumerate(a):
            seen = defaultdict(int)
            for cand in candidates:
                seen[data[cand][i]] += 1

            if seen["0"] > seen["1"]:
                lessc = "0"
            else:
                lessc = "1"
            print(f" Place {i} Winner {lessc} ")

            to_remove = []
            for cand in candidates:
                if data[cand][i] != lessc:
                    to_remove.append(cand)
            candidates -= set(to_remove)
            if len(candidates) == 1:
                lesscfull = data[list(candidates)[0]]
                break
            print(candidates)
            for cand in candidates:
                print(data[cand])
            print("--")

        # if len(data) < 15:
        #     print(data)
        o2 = int(lesscfull, 2)
        print(f"------> {co2} <----")
        print(f"------> {o2} <----")
        # (You guessed 3394305.)
        return co2 * o2
