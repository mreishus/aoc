#!/usr/bin/env python
"""
Advent Of Code 2024 Day 13
https://adventofcode.com/2024/day/13
"""
from typing import List
import re
from collections import namedtuple, defaultdict
from aoc.heapdict import heapdict
Spell = namedtuple("Spell", ("name", "cost", "damage", "heal", "effect_time"))

MachineState = namedtuple("MachineState", ("x", "y", "a_press", "b_press"))
def ms_to_loc(machine_state):
    return (machine_state.x, machine_state.y)

class Machine:
    def __init__(self, ax, ay, bx, by, px, py):
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.px = px
        self.py = py

    def advance_state(self, m_state, press):
        if press == 'a':
            return MachineState( m_state.x + self.ax, m_state.y + self.ay, m_state.a_press + 1, m_state.b_press )
        if press == 'b':
            return MachineState( m_state.x + self.bx, m_state.y + self.by, m_state.a_press, m_state.b_press + 1 )

    def solve(self):
        init_state = MachineState(0, 0, 0, 0)
        dist_to = defaultdict(lambda: 999_999)
        edge_to = {}
        open_set = heapdict()

        dist_to[ms_to_loc(init_state)] = 0
        open_set[init_state] = 0
        while len(open_set) > 0:
            (state, length) = open_set.popitem()

            if state.x == self.px and state.y == self.py:
                return length

            available_presses = []
            if state.a_press <= 100 and state.b_press <= 100:
                available_presses = ['a', 'b']
            elif state.a_press <= 100:
                available_presses = ['a']
            elif state.b_press <= 100:
                available_presses = ['b']
            else:
                return 0

            for press in available_presses:
                cost = 3
                if press == 'b':
                    cost = 1
                new_state = self.advance_state(state, press)

                new_state_loc = ms_to_loc(new_state)
                state_loc = ms_to_loc(state)
                if dist_to[new_state_loc] > dist_to[state_loc] + cost:
                    dist_to[new_state_loc] = dist_to[state_loc] + cost
                    edge_to[new_state] = (state, press)
                    open_set[new_state] = dist_to[new_state_loc]
        return 0

    def __str__(self):
        return f"#Machine({self.ax}, {self.ay})"
    def __repr__(self):
        return self.__str__()

def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

def parse(filename):
    with open(filename) as file:
        string = file.read()
    parts = string.split("\n\n")
    machines = []
    for p in parts:
        lines = p.split("\n")
        [ax, ay] = ints(lines[0])
        [bx, by] = ints(lines[1])
        [px, py] = ints(lines[2])
        machines.append( Machine( ax, ay, bx, by, px, py ) )
    return machines

class Day13:
    """AoC 2024 Day 13"""

    @staticmethod
    def part1(filename: str) -> int:
        machines = parse(filename)

        total = 0
        for m in machines:
            p1_for_m = m.solve()
            total += p1_for_m
            # print(m, p1_for_m)
        return total

    @staticmethod
    def part2(filename: str) -> int:
        return
