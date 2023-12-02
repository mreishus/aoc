#!/usr/bin/env python
"""
Advent Of Code 2023 Day 2
https://adventofcode.com/2023/day/1
"""
import re

PARSER = re.compile(r"^Game (\d+): (.*)$")


def parse(filename: str):
    data = {}
    with open(filename) as file:
        for line in file.readlines():
            (game_num, subsets) = parse_line(line.strip())
            data[game_num] = subsets
    return data


def parse_line(line):
    (game_num, rest) = re.search(PARSER, line).groups()
    subsets = rest.split("; ")

    parsed_subsets = []
    for raw_subset in subsets:
        this_subset = {}
        for pair in raw_subset.split(", "):
            (num, color) = re.search(r"(\d+) (\w+)", pair).groups()
            this_subset[color] = int(num)
        parsed_subsets.append(this_subset)
    return (int(game_num), parsed_subsets)


class Day02:
    """AoC 2023 Day 02"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        possible = []
        for game_num in data.keys():
            is_possible = True
            for subset in data[game_num]:
                if "red" in subset and subset["red"] > 12:
                    is_possible = False
                    break
                if "green" in subset and subset["green"] > 13:
                    is_possible = False
                    break
                if "blue" in subset and subset["blue"] > 14:
                    is_possible = False
                    break
            if is_possible:
                possible.append(game_num)

        return sum(possible)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)

        powers = []
        for game_num in data.keys():
            max_red = 0
            max_green = 0
            max_blue = 0
            for subset in data[game_num]:
                if "red" in subset and subset["red"] > max_red:
                    max_red = subset["red"]
                if "green" in subset and subset["green"] > max_green:
                    max_green = subset["green"]
                if "blue" in subset and subset["blue"] > max_blue:
                    max_blue = subset["blue"]
            powers.append(max_red * max_green * max_blue)
        return sum(powers)
