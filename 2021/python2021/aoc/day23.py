#!/usr/bin/env python
"""
Advent Of Code 2021 Day 23
https://adventofcode.com/2021/day/23
"""
from collections import namedtuple, defaultdict
import math

from aoc.heapdict import heapdict

# from heapdict import heapdict
from copy import deepcopy

State = namedtuple("State", ("podlocs"))
Edge = namedtuple("Edge", ("state", "length"))


class hashabledict(dict):
    def __key(self):
        return tuple((k, self[k]) for k in sorted(self))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()


class Maze:
    def __init__(self, filename):
        self.grid = {}
        self.podlocs = {}
        self.must_move = [(3, 1), (5, 1), (7, 1), (9, 1)]
        self.pods = ["A", "B", "C", "D", "A2", "B2", "C2", "D2"]
        self.parse(filename)

    def parse(self, filename):
        grid = defaultdict(lambda: " ")
        x = y = 0
        with open(filename) as f:
            for line in f:
                for char in line.strip("\n"):
                    if char in ["A", "B", "C", "D"]:
                        if char in self.podlocs:
                            char = char + "2"
                        self.podlocs[char] = (x, y)
                        grid[x, y] = "."
                    else:
                        grid[x, y] = char
                    x += 1
                y += 1
                x = 0
        self.grid = grid

    def solve(self):
        print("solve?")
        dist_to = defaultdict(lambda: math.inf)
        edge_to = {}
        queue = heapdict()

        state = State(hashabledict(deepcopy(self.podlocs)))
        dist_to[state] = 0
        queue[state] = 0

        while len(queue) > 0:
            (state, length) = queue.popitem()
            # print(f"Considering state: {state}")
            if is_winner(state):
                break

            steps = self.possible_edges(state)
            for new_state, length in steps:
                if dist_to[new_state] > dist_to[state] + length:
                    dist_to[new_state] = dist_to[state] + length
                    edge_to[new_state] = state
                    queue[new_state] = dist_to[new_state]

        print("==Done==")
        for k, v in dist_to.items():
            if is_winner(k):
                print("Found winner:")
                print(f"{v} {k}")
                return v

    # def display(self):
    #     for y in range(5):
    #         for x in range(13):
    #             print(self.grid[x, y], end="")
    #         print("")

    def possible_edges(self, state):
        podlocs = state.podlocs
        allpods = podlocs.values()

        # self.display()

        # Check if someone must move
        free_to_move = self.pods
        for pod in self.pods:
            if podlocs[pod] in self.must_move:
                free_to_move = [pod]
                break

        edges = []

        for pod in free_to_move:
            loc = podlocs[pod]
            # print(f"{pod} {loc}")
            for x, y in get_neighbors(loc):
                if self.grid[x, y] == "#":
                    continue
                if (x, y) in podlocs.values():
                    continue

                newlocs = deepcopy(podlocs)
                newlocs[pod] = (x, y)
                # print(f"--> {pod} moving to {x} {y}")
                new_state = State(newlocs)
                energy = get_energy(pod)
                edges.append(Edge(new_state, energy))

        return edges


def get_energy(pod):
    if pod == "A" or pod == "A2":
        return 1
    if pod == "B" or pod == "B2":
        return 1
    if pod == "C" or pod == "C2":
        return 1
    if pod == "D" or pod == "D2":
        return 1
    raise ValueError


def get_neighbors(loc):
    x, y = loc
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def is_winner(state: State):
    a = (state.podlocs["A"] == (3, 2) and state.podlocs["A2"] == (3, 3)) or (
        state.podlocs["A"] == (3, 3) and state.podlocs["A2"] == (3, 2)
    )
    b = (state.podlocs["B"] == (5, 2) and state.podlocs["B2"] == (5, 3)) or (
        state.podlocs["B"] == (5, 3) and state.podlocs["B2"] == (5, 2)
    )
    c = (state.podlocs["C"] == (7, 2) and state.podlocs["C2"] == (7, 3)) or (
        state.podlocs["C"] == (7, 3) and state.podlocs["C2"] == (7, 2)
    )
    d = (state.podlocs["D"] == (9, 2) and state.podlocs["D2"] == (9, 3)) or (
        state.podlocs["D"] == (9, 3) and state.podlocs["D2"] == (9, 2)
    )
    # print(state.podlocs)
    # print(a, b, c, d)
    return a and b and c and d


class Day23:
    """ AoC 2021 Day 23 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 23 part 1 """
        m = Maze(filename)
        print(m.grid)
        print(m.podlocs)
        m.solve()
        return -1

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 23 part 2 """
        return -1


if __name__ == "__main__":
    print(Day23.part1("/home/p22/h21/dev/aoc/2021/inputs/23/input_small2.txt"))
