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
    invalids_seen = set()

    low_digit_len = len(str(low))
    high_digit_len = len(str(high))

    repeat_len_low = 1
    repeat_len_high = max(low_digit_len, high_digit_len) // 2
    for repeat_len in range(repeat_len_low, repeat_len_high+1):
        orig_repeat = int('1' + ('0' * (repeat_len-1)))
        # print("Considering ", repeat_len, orig_repeat)

        times_low = low_digit_len // repeat_len
        times_high = high_digit_len // repeat_len
        for times in range(times_low, times_high+1):
            if times == 1:
                continue
            repeat = orig_repeat
            while True:
                s_repeat = str(repeat) # "12"
                if len(s_repeat) != repeat_len: # We got too big?
                    break
                candidate = int(s_repeat * times) # 121212121212
                if candidate >= low and candidate <= high and candidate not in invalids_seen:
                    # print("Adding ", candidate, "because", s_repeat, " times ", times)
                    invalids.append(candidate)
                    invalids_seen.add(candidate)
                if candidate > high:
                    break
                repeat += 1
    return invalids


class Day02:
    """AoC 2025 Day 02"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return solve1(data)
        # Manually submitted +11 because my program doesn't do # [1] [15]

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return solve2(data)
