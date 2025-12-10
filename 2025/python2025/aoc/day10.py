#!/usr/bin/env python
"""
Advent Of Code 2025 Day 10
https://adventofcode.com/2025/day/10
"""
from collections import defaultdict
import heapq
import random
from z3 import *

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
        joltage = tuple([int(x) for x in joltage_string.strip('{}').split(',')])
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
        # print('--')
        # print(machine)
        s = solve_machine(machine)
        if s is None:
            print("Bad")
            exit()
        r += s
    return r

def solve2(data):
    r = 0
    for machine in data:
        # print(machine)
        # # s = solve_machine(machine, True)
        # print(s)
        s2 = solve_buttons_z3(machine['buttons'], machine['joltage'])
        # print("S2: ", s2, sum(s2))
        r += sum(s2)
    return r

def solve_machine(machine, is_pt2=False):
    if not is_pt2:
        init_state = machine['lights']
    else:
        init_state = tuple([0] * len(machine['joltage']))

    dist_to = defaultdict(lambda: 999_999)
    edge_to = {}
    open_set = []

    dist_to[init_state] = 0
    heapq.heappush(open_set, (0, init_state))
    while len(open_set) > 0:
        (length, state) = heapq.heappop(open_set)
        if length > dist_to[state]:
            continue  # stale entry

        if (random.randint(1, 100000) == 42):
            print(state, " ", len(open_set))

        ## P1 end condition: All Falses
        if not is_pt2 and not any(state):
            return length
        ## P2 end condition: We hit the jotlage nums exactly
        if is_pt2 and state == machine['joltage']:
            return length

        if is_pt2 and is_hopeless(machine, state):
            continue

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

def is_hopeless(machine, state):
    for i, v in enumerate(state):
        if v > machine['joltage'][i]:
            return True
    return False

def next_states(machine, state, is_pt2=False):
    r = []
    for i, buttons in enumerate(machine['buttons']):
        new_state = list(state)

        ## Part 1 : Buttons toggle and cost is always 1
        if not is_pt2:
            for b in buttons:
                new_state[b] = not new_state[b]
            cost = 1
            r.append((tuple(new_state), cost, i))

        ## Part 2 : Buttons add jolts, cost is always 1 I guess..
        if is_pt2:
            for b in buttons:
                new_state[b] += 1
            cost = 1
            if not is_hopeless(machine, new_state):
                r.append((tuple(new_state), cost, i))
    return r

def solve_buttons_z3(buttons, joltage):
    n_vars = len(buttons)
    x = [Int(f'x{i}') for i in range(n_vars)]
    
    s = Optimize()
    
    # Everything is positive
    for xi in x:
        s.add(xi >= 0)
    
    # Joltage
    for j, target in enumerate(joltage):
        terms = []
        for i, btn in enumerate(buttons):
            if j in btn:
                terms.append(x[i])
        s.add(Sum(terms) == target)

    # Minimize total presses
    s.minimize(Sum(x))
    
    if s.check() == sat:
        m = s.model()
        return [m[xi].as_long() for xi in x]
    return None


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
