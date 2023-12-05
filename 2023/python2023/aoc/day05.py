#!/usr/bin/env python
"""
Advent Of Code 2023 Day 5
https://adventofcode.com/2023/day/5
"""
import re
from typing import List
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip()
        seeds, *raw_blocks = lines.split("\n\n")
        seeds = ints(seeds)

        block_map = {}
        for block in raw_blocks:
            _from, _to, data = parse_block(block)
            block_map[_from] = (_to, data)
        return (seeds, block_map)


def parse_block(block):
    lines = block.split("\n")
    label = lines[0]
    label = label.split(" ")[0]
    from_, to_ = label.split("-to-")

    data = []
    for line in lines[1:]:
        dest_start, source_start, length = ints(line)
        source_end = source_start + length - 1
        offset = dest_start - source_start
        data.append([dest_start, source_start, length, source_end, offset])
    data = sorted(data, key=lambda x: x[1])
    return from_, to_, data


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def seed_to(target: str, x: int, block_map: dict):
    have = "seed"
    while have != target:
        (next_have, data) = block_map[have]

        for dest_start, source_start, length, source_end, offset in data:
            if source_start <= x <= source_end:
                x += offset
                break
            if source_start > x:
                break
        have = next_have
    return x


class Day05:
    """AoC 2023 Day 05"""

    @staticmethod
    def part1(filename: str) -> int:
        (seeds, block_map) = parse(filename)

        location_min = float("inf")
        for i in seeds:
            loc = seed_to("location", i, block_map)
            location_min = min(location_min, loc)
        return location_min

    @staticmethod
    def part2(filename: str) -> int:
        (seeds, block_map) = parse(filename)

        location_min = float("inf")
        for i in range(0, len(seeds), 2):
            seeds_range = list(range(seeds[i], seeds[i] + seeds[i + 1]))

            for j in seeds_range:
                loc = seed_to("location", j, block_map)
                location_min = min(location_min, loc)
        return location_min
