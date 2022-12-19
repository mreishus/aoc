#!/usr/bin/env python
"""
Advent Of Code 2022 Day 19
https://adventofcode.com/2022/day/19
"""
import re
from typing import NamedTuple
from collections import deque, defaultdict

PARSER = re.compile(r"Each (\w+) robot costs (\d+) (\w+)( and (\d+) (\w+))?")

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
LOOKUP = {
    "ore": ORE,
    "clay": CLAY,
    "obsidian": OBSIDIAN,
    "geode": GEODE,
}


State = NamedTuple(
    "State",
    [
        ("ores", tuple),
        ("bots", tuple),
        ("minutes", int),
    ],
)


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    rules = {}
    matches = re.findall(PARSER, line)
    for match in matches:
        # Examples:
        # ('ore', '2', 'ore', '', '', '')
        # ('obsidian', '3', 'ore', ' and 8 clay', '8', 'clay')
        val = [0, 0, 0, 0]
        val[LOOKUP[match[2]]] = int(match[1])
        if match[4] != "":
            val[LOOKUP[match[5]]] = int(match[4])
        rules[LOOKUP[match[0]]] = val

    ## rules looks like: {0: [4, 0, 0, 0], 1: [4, 0, 0, 0], 2: [4, 15, 0, 0], 3: [3, 0, 8, 0]}
    return rules


def init_state():
    return State(
        ores=(0, 0, 0, 0),
        bots=(1, 0, 0, 0),
        minutes=0,
    )


def get_neighbors(state, rules):
    ## Determine the Ore Deltas before we buy any bots
    ore_deltas = [0, 0, 0, 0]
    for i in range(4):
        ore_deltas[i] += state.bots[i]

    can_affords = [False, False, False, False]
    for i in range(4):
        costs = rules[i]  # [ore, clay, obsidian, geode]
        afford_component = [None, None, None, None]
        for j in range(4):
            if costs[j] == 0:
                continue
            afford_component[j] = state.ores[j] // costs[j]
        can_affords[i] = min([x for x in afford_component if x is not None])

    new_states = []

    # What if I don't buy anything
    if not (can_affords[3]):
        new_state = State(
            ores=tuple([state.ores[i] + ore_deltas[i] for i in range(4)]),
            bots=state.bots,
            minutes=state.minutes + 1,
        )
        new_states.append(new_state)

    # Try to buy each one
    for i in reversed(range(4)):
        if not can_affords[i]:
            continue

        ## If the highest cost for clay is 10, and I have 10 clay bots,
        ## I don't need any more clay bots
        if i < 3:
            current_bots = state.bots[i]
            max_cost_for_resource_i = max([x[i] for x in rules.values()])
            if current_bots >= max_cost_for_resource_i:
                continue

        new_ores = list(state.ores)
        new_bots = list(state.bots)
        for j in range(4):
            new_ores[j] -= rules[i][j]
            new_ores[j] += ore_deltas[j]
        new_bots[i] += 1
        new_state = State(
            ores=tuple(new_ores),
            bots=tuple(new_bots),
            minutes=state.minutes + 1,
        )
        new_states.append(new_state)
        # Optimization: If we can afford a geode, don't bother with others
        if i == 3:
            break
    return new_states


def test_blueprint(rules, max_minutes):
    init = init_state()
    q = deque([init])
    q_by_bots_and_minutes = defaultdict(set)
    q_by_bots_and_minutes[(init.bots, init.minutes)].add(init)
    geodes_by_minutes = defaultdict(int)

    seen = set()
    final_states = []

    i = 0

    parent_of = {}

    while q:
        s = q.popleft()
        # print("s", s)
        # print("q", q_by_bots_and_minutes)
        q_by_bots_and_minutes[(s.bots, s.minutes)].remove(s)
        if s in seen:
            continue
        seen.add(s)

        found_better = False
        for other_state in q_by_bots_and_minutes[(s.bots, s.minutes)]:
            if strictly_greater(other_state.ores, s.ores):
                found_better = True
                break

        if (s.ores[GEODE] + 1) < geodes_by_minutes[s.minutes]:
            found_better = True

        if found_better:
            continue

        geodes_by_minutes[s.minutes] = max(geodes_by_minutes[s.minutes], s.ores[GEODE])

        i += 1
        if i % 100000 == 0:
            maxp = 0
            if len(final_states) > 0:
                m = max(final_states, key=lambda s: s.ores[GEODE])
                maxp = m.ores[GEODE]
            print(
                f"Seen {i} states | {len(q)} in queue | {len(seen)} seen | s.minutes={s.minutes} | current max {maxp}"
            )
            # for qq in q:
            #     print(qq)
            # exit()

        if s.minutes == max_minutes:
            final_states.append(s)
            continue

        for n in get_neighbors(s, rules):
            if n in seen:
                continue

            examine = q_by_bots_and_minutes[(n.bots, n.minutes)]
            found_better = False
            for other_state in examine:
                if strictly_greater(other_state.ores, n.ores):
                    found_better = True
                    break
            if found_better:
                continue

            q.append(n)
            parent_of[n] = s
            q_by_bots_and_minutes[(n.bots, n.minutes)].add(n)

    m = max(final_states, key=lambda s: s.ores[GEODE])
    print("We can get ", m.ores[GEODE], " geodes in ", m.minutes, " minutes")

    # print("How we got there: ")
    # z = m
    # while z in parent_of:
    #     print(z)
    #     z = parent_of[z]

    return m.ores[GEODE]


def strictly_greater(a, b):
    """Returns True if a > b"""
    if a[GEODE] > b[GEODE]:
        return True

    for i in range(len(a)):
        if a[i] < b[i]:
            return False
    return True


class Day19:
    """AoC 2022 Day 19"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        total_quality = 0
        for i, bp in enumerate(data, 1):
            geodes = test_blueprint(bp, 24)
            quality = i * geodes
            total_quality += quality
        return total_quality

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        product = 1
        product *= test_blueprint(data[0], 32)
        product *= test_blueprint(data[1], 32)
        if len(data) > 2:
            product *= test_blueprint(data[2], 32)
        return product
