#!/usr/bin/env python
"""
Advent Of Code 2025 Day 10
https://adventofcode.com/2025/day/10
"""
from collections import defaultdict
import heapq

def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip().split("\n")

    r = []
    for line in lines:
        parts = line.split(" ")
        lights_string = parts[0]
        lights = [c == '#' for c in lights_string.strip('[]')]

        l = len(parts)
        buttons_string = parts[1:l-1]
        buttons = [[int(x) for x in s.strip('()').split(',')] for s in buttons_string]

        joltage_string = parts[-1]
        joltage = [int(x) for x in joltage_string.strip('{}').split(',')]
        item = {
            'lights': tuple(lights),
            'buttons': buttons,
            'joltage': joltage,
        }
        r.append(item)
    return r

def solve1(data):
    r = 0
    for machine in data:
        print('--')
        print(machine)
        s = solve_machine(machine)
        if s is None:
            print("Bad")
            exit()
        r += s
    return r

def solve2(data):
    return -1

def solve_machine(machine, is_pt2=False):
    init_state = machine['lights']
    dist_to = defaultdict(lambda: 999_999)
    edge_to = {}
    open_set = []

    dist_to[init_state] = 0
    heapq.heappush(open_set, (0, init_state))
    while len(open_set) > 0:
        (length, state) = heapq.heappop(open_set)
        if length > dist_to[state]:
            continue  # stale entry

        # if all(state):
        if not any(state):
            return length

        # print("")
        # print(f"Looking from: {state}")
        for new_state, cost, name in next_states(machine, state, is_pt2):
            # print(f"  Pressing {name} gets {new_state})")
            if dist_to[new_state] > dist_to[state] + cost:
                dist_to[new_state] = dist_to[state] + cost
                edge_to[new_state] = (state, name)
                heapq.heappush(open_set, (dist_to[new_state], new_state))
                # print("Added to queue")

    return None

def next_states(machine, state, is_pt2=False):
    r = []
    for i, buttons in enumerate(machine['buttons']):
        new_state = list(state)
        for b in buttons:
            new_state[b] = not new_state[b]
        cost = 1
        r.append((tuple(new_state), cost, i))
    return r


class Day10:
    """AoC 2025 Day 10"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return solve1(data)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return solve2(data)
        # g = Grid()
        # return g.solve2(data)
