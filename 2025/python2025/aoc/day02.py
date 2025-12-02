#!/usr/bin/env python
"""
Advent Of Code 2025 Day 2
https://adventofcode.com/2025/day/2
"""

def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip().split("\n")
    r = []
    for rng in lines[0].split(","):
        left, right = rng.split('-')
        r.append((int(left), int(right)))
    return r

def solve1(data):
    total = 0
    for low, high in data:
        # print(low, high)
        for id in get_invalid_ids(low, high):
            # print(f"   ---> id={id}")
            total += id
    return total

def get_invalid_ids(low, high):
    # print(f"--> Get invalids [{low}] [{high}]")
    digit_len = len(str(low))
    if digit_len == 1:
        half = low
    else:
        half = int(str(low)[0:digit_len//2])

    ## Fix for odd digit lengths
    if digit_len % 2 == 1 and digit_len > 2:
        half = inc_until_one_digit_longer(half)

    # print("")
    # print(f"digit len={digit_len} first half={half}")

    invalids = []
    while True:
        shalf = str(half)
        candidate = int(shalf + shalf)
        if candidate >= low and candidate <= high:
            invalids.append(candidate)
        if candidate > high:
            break
        half += 1
    return invalids

def inc_until_one_digit_longer(num):
    original_len = len(str(num))
    while True:
        num += 1
        if len(str(num)) > original_len:
            return num

def solve2(data):
    total = 0
    for low, high in data:
        # print(low, high)
        for id in get_invalid_ids2(low, high):
            # print(f"   ---> id={id}")
            total += id
    return total

def get_invalid_ids2(low, high):
    # print(f"--> Get invalids [{low}] [{high}]")
    invalids = []
    seen = set()

    low_digits = len(str(low))
    high_digits = len(str(high))

    max_block_len = max(low_digits, high_digits) // 2
    for block_len in range(1, max_block_len+1):
        # Smallest possible block with this length (1, 10, 100.. etc)
        block_start = int('1' + ('0' * (block_len-1)))
        # print("Considering ", block_len, block_start)

        ## Min/max times we can repeat the block, given digit lengths
        min_times = low_digits // block_len
        max_times = high_digits // block_len
        for times in range(min_times, max_times+1):
            # Repeating once isn't "repeated"
            if times == 1:
                continue
            block = block_start
            while True:
                block_str = str(block) # "12"
                if len(block_str) != block_len: # We got too big?
                    break
                candidate = int(block_str * times) # 121212121212
                if candidate >= low and candidate <= high and candidate not in seen:
                    # print("Adding ", candidate, "because", block_str, " times ", times)
                    invalids.append(candidate)
                    seen.add(candidate)
                if candidate > high:
                    break
                block += 1
    return invalids


class Day02:
    """AoC 2025 Day 02"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return solve1(data)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return solve2(data)
