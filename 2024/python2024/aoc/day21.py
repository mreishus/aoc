#!/usr/bin/env python
"""
Advent Of Code 2024 Day 21
https://adventofcode.com/2024/day/21
"""
from functools import lru_cache
from aoc.heapdict import heapdict
from collections import defaultdict, namedtuple

class Hashabledict(dict):
    def __hash__(self):
        return hash(frozenset(self)) # only covers keys, trust needed

State = namedtuple("State", ("numloc", "code", "arrowloc"))

class KeypadNum:
    def __init__(self):
        self.grid = {
            (0, 0): 7,
            (1, 0): 8,
            (2, 0): 9,
            (0, 1): 4,
            (1, 1): 5,
            (2, 1): 6,
            (0, 2): 1,
            (1, 2): 2,
            (2, 2): 3,
            # (0, 3): ?, # Not there
            (1, 3): 0,
            (2, 3): 'A',
        }
        self.begin_loc = (2, 3)
        self.begin_loc_keypad = (2, 0)

    def search(self, final_code):
        self.target_code = tuple(list(final_code))
        final_code = tuple(list(final_code))

        # init_state = (self.begin_loc, ())
        init_state = State(self.begin_loc, (), self.begin_loc_keypad)

        dist_to = defaultdict(lambda: 999_999)
        edge_to = defaultdict(list)  # a list of previous states for each state
        open_set = heapdict()
        dist_to[init_state] = 0
        open_set[init_state] = 0
        final_state = None  # Store the final state when we find it

        while len(open_set) > 0:
            (state, length) = open_set.popitem()
            (numloc, code, arrowloc) = state
            if code == final_code:
                final_state = state
                break  # We found our target
            for (new_state, cost, name) in self.next_states(state):
                if dist_to[new_state] > dist_to[state] + cost:
                    dist_to[new_state] = dist_to[state] + cost
                    edge_to[new_state] = (state, name)
                    open_set[new_state] = dist_to[new_state]

        if final_state is None:
            return 0

        # Reconstruct the path
        path = []
        current_state = final_state
        while current_state in edge_to:
            prev_state, move = edge_to[current_state]
            path.append(move)
            current_state = prev_state

        path.reverse()  # Since we built it backwards
        return len(path), path

    def next_states(self, state):
        numloc = state.numloc
        output = state.code
        arrowloc = state.arrowloc

        (x, y) = numloc
        dirs = {
            '^': (0, -1),
            'v': (0, 1),
            '<': (-1, 0),
            '>': (1, 0),
        }
        for (dir_name, (dx, dy)) in dirs.items():
            if (dx+x, dy+y) in self.grid:
                new_state = State((dx+x, dy+y), output, arrowloc)
                yield new_state, 1, dir_name

        # Only allow pressing 'A' if the resulting code would still be a valid prefix
        digit = str(self.grid[numloc])
        new_output = tuple(list(output) + [digit])
        if len(new_output) <= len(self.target_code) and all(a == b for a, b in zip(new_output, self.target_code)):
            new_state = State(numloc, new_output, arrowloc)
            yield new_state, 1, 'A'


class KeypadArrow:
    def __init__(self):
        self.grid = {}

    def fill(self):
        self.grid = {
            #(0, 0): 7, # Not There
            (1, 0): '^',
            (2, 0): 'A',
            (0, 1): '<',
            (1, 1): 'v',
            (2, 1): '>',
        }
        self.begin_loc = (2, 0)


def parse(filename):
    with open(filename) as file:
        string = file.read().strip()
    return string.split("\n")

class Day21:
    """AoC 2024 Day 21"""

    @staticmethod
    def part1(filename: str) -> int:
        kn = KeypadNum()
        print(kn.search( '029A' ))

        # stuff = parse(filename)
        # print(stuff)
        return -1

    @staticmethod
    def part2(filename: str) -> int:
        pass
