#!/usr/bin/env python
"""
Advent Of Code 2022 Day 19
https://adventofcode.com/2022/day/19
"""
from typing import List
import re
from dataclasses import dataclass
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


class Blueprint:
    def __init__(self, rules):
        self.rules = rules


State = NamedTuple(
    "State",
    [
        ("ores", tuple),
        ("bots", tuple),
        ("minutes", int),
    ],
)


def freeze_dict(d):
    # return tuple((k, d[k]) for k in sorted(d.keys()))
    return tuple((k, tuple(d[k])) for k in sorted(d.keys()))


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    print(line)
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

    print(rules)
    return Blueprint(rules)


def init_state(bp):
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

    def something(this_state, i):
        """Decide how many new bots of type i to buy"""
        costs = rules[i]  # [ore, clay, obsidian, geode]
        affords = [None, None, None, None]
        for j in range(4):
            if costs[j] == 0:
                continue
            else:
                affords[j] = this_state.ores[j] // costs[j]
        can_afford = min([x for x in affords if x is not None])
        # print(
        #     f"--> Can afford {can_afford} of {i}. [ores: {this_state.ores}] [costs: {costs}] [affords: {affords}]"
        # )

        new_states = []
        # for buy_qty in range(can_afford + 1):
        # ^^ Old idea, try every possible purchase combination
        # vv Min max idea, either buy 0 or max for each type of bot
        for buy_qty in [0, can_afford]:
            new_ores = list(this_state.ores)
            new_bots = list(this_state.bots)
            for j in range(4):
                new_ores[j] -= buy_qty * costs[j]
            new_bots[i] += buy_qty

            minutes_delta = 0
            if i == 3:
                minutes_delta = 1

            new_state = State(
                ores=tuple(new_ores),
                bots=tuple(new_bots),
                minutes=state.minutes + minutes_delta,
            )
            if i < 3:
                these_new_states = something(new_state, i + 1)
                new_states.extend(these_new_states)
            else:
                new_states.append(new_state)
        return new_states

    ## Process all buying decisions
    new_states = something(state, 0)

    ## Increment ores
    for i in range(len(new_states)):
        ns = new_states[i]
        new_states[i] = State(
            ores=tuple([ns.ores[j] + ore_deltas[j] for j in range(4)]),
            bots=ns.bots,
            minutes=ns.minutes,
        )

    # print("new_states: ")
    # for i, ns in enumerate(new_states):
    #     print(ns)
    # print("---")

    return new_states


def test_blueprint(bp):
    max_minutes = 24

    init = init_state(bp)
    q = deque([init])
    q_by_bots_and_minutes = defaultdict(set)
    q_by_bots_and_minutes[(init.bots, init.minutes)].add(init)

    seen = set()
    final_states = []
    rules = bp.rules

    i = 0

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
        if found_better:
            continue

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
                    # print(" SBSBSBSB ", other_state)
                    found_better = True
                    break
            if found_better:
                # print()
                # print("------")
                # print("Not adding because we found a better state")
                # print("This one wasn't added: ")
                # print(n)
                # print("We were looking at these:")
                # for other_state in examine:
                #     print(other_state)
                # print("------")
                # print()
                continue

            q.append(n)
            q_by_bots_and_minutes[(n.bots, n.minutes)].add(n)

    # m = max(final_states, key=lambda s: s.ores[CLAY])
    # print("We can get ", m.ores[CLAY], " clay in ", m.minutes, " minutes")
    m = max(final_states, key=lambda s: s.ores[GEODE])
    print("We can get ", m.ores[GEODE], " geodes in ", m.minutes, " minutes")
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
            geodes = test_blueprint(bp)
            quality = i * geodes
            total_quality += quality
        return total_quality

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        if len(data) <= 20:
            print(data)
        return -2
