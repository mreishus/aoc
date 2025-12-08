#!/usr/bin/env python
"""
Advent Of Code 2025 Day 8
https://adventofcode.com/2025/day/8
"""
import math
import heapq

def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip().split("\n")
    r = []
    for line in lines:
        r.append(list(map(int, line.split(","))))
    return r

def distance(p1, p2):
    [a, b, c] = p1
    [x, y, z] = p2
    d2 = (x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2
    return math.sqrt(d2)

def solve1(data, num_to_connect):
    heap = []
    for i in range(len(data)):
        # print(i, data[i])
        for j in range(i+1, len(data)):
            d = distance(data[i], data[j])
            heapq.heappush(heap, (d, i, j))

    circuits = []
    for _ in range(num_to_connect):
        dist, i, j = heapq.heappop(heap)
        # print(dist, i, j, data[i], data[j])

        matched_circuits = []
        for c, cir in enumerate(circuits):
            if i in cir or j in cir:
                matched_circuits.append(c)
        if len(matched_circuits) == 0:
            new_cir = set()
            circuits.append(new_cir)
            matched_circuits = [ len(circuits) - 1 ]
        if len(matched_circuits) == 1:
            circuits[matched_circuits[0]] |= set([i, j])
        elif len(matched_circuits) > 1:
            ## Add to lowest cir
            circuits[matched_circuits[0]] |= set([i, j])
            ## Merge higher circs into it
            for x in reversed(sorted(matched_circuits[1:])):
                circuits[matched_circuits[0]] |= circuits[x]
                del circuits[x]

    biggest_three_sizes = sorted((len(s) for s in circuits), reverse=True)[:3]
    return biggest_three_sizes[0] * biggest_three_sizes[1] * biggest_three_sizes[2]

def solve2(data):
    heap = []
    for i in range(len(data)):
        # print(i, data[i])
        for j in range(i+1, len(data)):
            d = distance(data[i], data[j])
            heapq.heappush(heap, (d, i, j))

    circuits = []
    last_i, last_j = None, None
    while len(circuits) != 1 or len(circuits[0]) != len(data):
        dist, i, j = heapq.heappop(heap)
        last_i, last_j = i, j
        # print(dist, i, j, data[i], data[j])

        matched_circuits = []
        for c, cir in enumerate(circuits):
            if i in cir or j in cir:
                matched_circuits.append(c)
        if len(matched_circuits) == 0:
            new_cir = set()
            circuits.append(new_cir)
            matched_circuits = [ len(circuits) - 1 ]
        if len(matched_circuits) == 1:
            circuits[matched_circuits[0]] |= set([i, j])
        elif len(matched_circuits) > 1:
            ## Add to lowest cir
            circuits[matched_circuits[0]] |= set([i, j])
            ## Merge higher circs into it
            for x in reversed(sorted(matched_circuits[1:])):
                circuits[matched_circuits[0]] |= circuits[x]
                del circuits[x]

    return data[last_i][0] * data[last_j][0]


class Day08:
    """AoC 2025 Day 08"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        # print(data)
        return solve1(data, 1000)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return solve2(data)

