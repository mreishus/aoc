#!/usr/bin/env python
"""
Advent Of Code 2023 Day 5
https://adventofcode.com/2023/day/5
"""
import re
from typing import List


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


def binary_search(data, x):
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        dest_start, source_start, length, source_end, offset = data[mid]

        if source_start <= x <= source_end:
            return mid
        elif x < source_start:
            high = mid - 1
        else:
            low = mid + 1
    return None


def seed_to(target: str, x: int, block_map: dict):
    have = "seed"
    while have != target:
        (next_have, data) = block_map[have]

        # Linear search replaced by binary search
        # for dest_start, source_start, length, source_end, offset in data:
        #     if source_start <= x <= source_end:
        #         x += offset
        #         break
        #     if source_start > x:
        #         break

        index = binary_search(data, x)
        if index is not None:
            _, source_start, _, source_end, offset = data[index]
            x += offset

        have = next_have
    return x


class Day05:
    """AoC 2023 Day 05"""

    @staticmethod
    def part1(filename: str) -> int:
        (seeds, block_map) = parse(filename)

        location_min = 9999999999
        for i in seeds:
            loc = seed_to("location", i, block_map)
            location_min = min(location_min, loc)
        return location_min

    @staticmethod
    def part2_large(seeds, block_map) -> int:
        location_min = 9999999999
        j_min = 9999999999

        ## Pass 1: Stride 1_000_000
        for i in range(0, len(seeds), 2):
            stride = 1_000_000
            seeds_range = range(seeds[i], seeds[i] + seeds[i + 1], stride)
            for j in seeds_range:
                loc = seed_to("location", j, block_map)
                if loc < location_min:
                    location_min = loc
                    j_min = j

        seed_low = None
        seed_high = None
        ## Pass 2: We're only interested in the seed range that contains the j_min found in pass 1
        for i in range(0, len(seeds), 2):
            stride = 1
            seeds_range = range(seeds[i], seeds[i] + seeds[i + 1], stride)

            if j_min in seeds_range:
                seed_low = seeds[i]
                seed_high = seeds[i] + seeds[i + 1]
                break

        if seed_low is None or seed_high is None:
            raise Exception("couldn't find seed range")

        ## Pass 3: Stride 10_000, but only in the seed range we're interested in
        for j in range(seed_low, seed_high, 10_000):
            loc = seed_to("location", j, block_map)
            if loc < location_min:
                location_min = loc
                j_min = j

        ## Pass 4:  +/- 5_000 around the j_min found in pass 3
        for j in range(j_min - 5_000, j_min + 5_000):
            loc = seed_to("location", j, block_map)
            if loc < location_min:
                location_min = loc
                j_min = j

        # print(f"found loc={location_min}, at j={j_min}")
        return location_min

    @staticmethod
    def part2_small(seeds, block_map) -> int:
        location_min = 9999999999
        for i in range(0, len(seeds), 2):
            seeds_range = range(seeds[i], seeds[i] + seeds[i + 1])
            for j in seeds_range:
                loc = seed_to("location", j, block_map)
                location_min = min(location_min, loc)

        return location_min

    @staticmethod
    def part2(filename: str) -> int:
        (seeds, block_map) = parse(filename)
        if seeds[1] > 1_000_000:
            return Day05.part2_large(seeds, block_map)
        return Day05.part2_small(seeds, block_map)
