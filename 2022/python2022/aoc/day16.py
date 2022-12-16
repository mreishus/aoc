#!/usr/bin/env python
"""
Advent Of Code 2022 Day 16
https://adventofcode.com/2022/day/16
"""
import re
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import NamedTuple

PARSER = re.compile(
    r"Valve (\w+) has flow rate=(\d+); tunnel(?:s)? lead(?:s)? to valve(?:s)? (.*)"
)

MAX_MINUTES = 30


@dataclass()
class Valve:
    name: str
    flow_rate: int


# @dataclass()
# class State:
#     loc: str
#     open_valves: set[str]
#     pressure_released: int
#     minutes: int
State = NamedTuple(
    "State",
    [
        ("loc", str),
        ("open_valves", frozenset),
        ("pressure_released", int),
        ("minutes", int),
    ],
)
StateNoPres = NamedTuple(
    "StateNoPres",
    [
        ("loc", str),
        ("open_valves", frozenset),
        ("minutes", int),
    ],
)


def get_state_no_press(s):
    # return StateNoPres(s.loc, s.open_valves, s.minutes)
    return StateNoPres("XYZ", s.open_valves, s.minutes)


def parse(filename):
    valves = {}
    vmap = defaultdict(list)

    with open(filename) as file:
        for line in file.readlines():
            line = line.strip()

            (valve, flow, tunnels) = re.search(PARSER, line).groups()
            flow = int(flow)
            valves[valve] = Valve(valve, flow)

            tunnels = tunnels.split(", ")
            for dest_tunnel in tunnels:
                vmap[valve].append(dest_tunnel)

    return valves, vmap


def init_state():
    return State("AA", frozenset(), 0, 0)


def get_neighbors(s, valves, vmap):
    if s.minutes >= MAX_MINUTES:
        return []

    r = []

    pressure_delta = 0
    for ov in s.open_valves:
        pressure_delta += valves[ov].flow_rate
    new_pressure = s.pressure_released + pressure_delta

    ## Moving to another valve
    for dest in vmap[s.loc]:
        r.append(State(dest, s.open_valves, new_pressure, s.minutes + 1))

    ## Opening a valve
    if s.loc not in s.open_valves:
        r.append(State(s.loc, s.open_valves | {s.loc}, new_pressure, s.minutes + 1))

    return r


def p1(valves, vmap):
    q = deque([init_state()])
    seen = set()
    i = 0

    final_states = []
    max_press_for = defaultdict(int)

    while q:
        s = q.popleft()  # BFS
        # s = q.pop()  # DFS

        ## Skip if we've seen this state before
        if s in seen:
            continue
        seen.add(s)

        ## Skip if we've seen this state before, but with more pressure
        snp = get_state_no_press(s)
        if s.pressure_released < max_press_for[snp]:
            continue
        max_press_for[snp] = s.pressure_released

        i += 1
        if i % 100000 == 0:
            maxp = 0
            if len(final_states) > 0:
                maxp = max(s.pressure_released for s in final_states)
            print(
                f"Seen {i} states | {len(q)} in queue | {len(seen)} seen | s.minutes={s.minutes} | current max {maxp}"
            )

        for n in get_neighbors(s, valves, vmap):
            q.append(n)

        if s.minutes >= MAX_MINUTES:
            final_states.append(s)

    m = max(final_states, key=lambda s: s.pressure_released)
    print(m)
    return m.pressure_released


class Day16:
    """AoC 2022 Day 16"""

    @staticmethod
    def part1(filename: str) -> int:
        valves, vmap = parse(filename)
        return p1(valves, vmap)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        if len(data) <= 20:
            print(data)
        return -2
