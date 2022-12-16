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


State = NamedTuple(
    "State",
    [
        ("loc", str),
        ("open_valves", frozenset),
        ("pressure_released", int),
        ("minutes", int),
        ("last_loc", str),
    ],
)
StateNoLastLoc = NamedTuple(
    "StateNoLastLoc",
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


def get_state_no_last_loc(s):
    return StateNoLastLoc(s.loc, s.open_valves, s.pressure_released, s.minutes)


def reverse_me_and_ele(snll):
    locs = snll.loc.split(",")
    locs = f"{locs[1]},{locs[0]}"
    return StateNoLastLoc(locs, snll.open_valves, snll.pressure_released, snll.minutes)


def get_state_no_press(s):
    # return StateNoPres(s.loc, s.open_valves, s.minutes)
    # return StateNoPres(s.loc, frozenset(), s.minutes)
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
    return State("AA", frozenset(), 0, 0, "")


def init_state_ele():
    return State("AA,AA", frozenset(), 0, 0, ",")


def get_neighbors(s, valves, vmap):
    if s.minutes >= MAX_MINUTES:
        return []

    r = []
    last_loc = s.loc

    pressure_delta = 0
    for ov in s.open_valves:
        pressure_delta += valves[ov].flow_rate
    new_pressure = s.pressure_released + pressure_delta

    ## Moving to another valve
    for dest in vmap[s.loc]:
        if dest == s.last_loc:
            continue
        r.append(State(dest, s.open_valves, new_pressure, s.minutes + 1, last_loc))

    ## Opening a valve
    if s.loc not in s.open_valves and valves[s.loc].flow_rate > 0:
        r.append(
            State(s.loc, s.open_valves | {s.loc}, new_pressure, s.minutes + 1, last_loc)
        )

    return r


def get_neighbors_ele(s, valves, vmap):
    if s.minutes >= MAX_MINUTES:
        return []

    r = []

    last_loc_me, last_loc_ele = s.last_loc.split(",")
    loc_me, loc_ele = s.loc.split(",")

    pressure_delta = 0
    for ov in s.open_valves:
        pressure_delta += valves[ov].flow_rate
    new_pressure = s.pressure_released + pressure_delta

    ## (ME+Ele) Moving to another valve
    my_acts = []
    ele_acts = []
    for dest_me in vmap[loc_me]:
        if dest_me == last_loc_me:
            continue
        my_acts.append(["move", dest_me])

    for dest_ele in vmap[loc_ele]:
        if dest_ele == last_loc_ele:
            continue
        ele_acts.append(["move", dest_ele])

        # r.append(
        #     State(
        #         f"{dest_me},{dest_ele}",
        #         s.open_valves,
        #         new_pressure,
        #         s.minutes + 1,
        #         s.loc,
        #     )
        # )

    ## Opening a valve
    if loc_me not in s.open_valves and valves[loc_me].flow_rate > 0:
        my_acts.append(["open", loc_me])
    if loc_ele not in s.open_valves and valves[loc_ele].flow_rate > 0:
        ele_acts.append(["open", loc_ele])

        # r.append(
        #     State(s.loc, s.open_valves | {s.loc}, new_pressure, s.minutes + 1, last_loc)
        # )

    for my_act in my_acts:
        for ele_act in ele_acts:

            new_open_valves = s.open_valves
            if my_act[0] == "open":
                new_open_valves = new_open_valves | {my_act[1]}
            if ele_act[0] == "open":
                new_open_valves = new_open_valves | {ele_act[1]}

            new_loc_me = loc_me
            new_loc_ele = loc_ele
            if my_act[0] == "move":
                new_loc_me = my_act[1]
            if ele_act[0] == "move":
                new_loc_ele = ele_act[1]

            r.append(
                State(
                    f"{new_loc_me},{new_loc_ele}",
                    new_open_valves,
                    new_pressure,
                    s.minutes + 1,
                    s.loc,
                )
            )

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
        snll = get_state_no_last_loc(s)
        if snll in seen:
            continue
        seen.add(snll)

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

        # print(s)
        for n in get_neighbors(s, valves, vmap):
            # print("--> ", n)
            q.append(n)

        if s.minutes >= MAX_MINUTES:
            final_states.append(s)

    m = max(final_states, key=lambda s: s.pressure_released)
    print(m)
    return m.pressure_released


def p2(valves, vmap):
    q = deque([init_state_ele()])
    seen = set()
    i = 0

    final_states = []
    max_press_for = defaultdict(int)

    while q:
        s = q.popleft()  # BFS
        # s = q.pop()  # DFS

        ## Skip if we've seen this state before
        snll = get_state_no_last_loc(s)
        if snll in seen:
            continue
        seen.add(snll)
        seen.add(reverse_me_and_ele(snll))

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

        # print(s)
        for n in get_neighbors_ele(s, valves, vmap):
            # print("--> ", n)
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
        global MAX_MINUTES
        MAX_MINUTES = 30
        return p1(valves, vmap)

    @staticmethod
    def part2(filename: str) -> int:
        valves, vmap = parse(filename)
        global MAX_MINUTES
        MAX_MINUTES = 26
        return p2(valves, vmap)
