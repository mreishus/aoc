#!/usr/bin/env python
"""
Advent Of Code 2021 Day 23
https://adventofcode.com/2021/day/23
"""
from collections import namedtuple, defaultdict
import math

from aoc.heapdict import heapdict

# from heapdict import heapdict

# from copy import deepcopy

State = namedtuple("State", ("podlocs"))
Edge = namedtuple("Edge", ("state", "length"))


class Maze:
    def __init__(self, filename):
        self.grid = {}
        self.podlocs = [
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
        ]
        self.must_move = [(3, 1), (5, 1), (7, 1), (9, 1)]
        self.pods = ["A", "A2", "B", "B2", "C", "C2", "D", "D2"]
        self.parse(filename)

    def podi(self, pod):
        return self.pods.index(pod)

    def parse(self, filename):
        grid = defaultdict(lambda: " ")
        x = y = 0
        with open(filename) as f:
            for line in f:
                for char in line.strip("\n"):
                    if char in ["A", "B", "C", "D"]:
                        if self.podlocs[self.podi(char)] != (0, 0):
                            char = char + "2"
                        self.podlocs[self.podi(char)] = (x, y)
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

        state = State(tuple(self.podlocs))
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

        # self.display()

        # Check if someone must move
        free_to_move = list(range(len(podlocs)))
        for i in range(len(podlocs)):
            if podlocs[i] in self.must_move:
                free_to_move = [i]

        edges = []
        for pod in free_to_move:
            loc = podlocs[pod]
            # print(f"{pod} {loc}")
            for x, y in get_neighbors(loc):
                if self.grid[x, y] == "#":
                    continue
                if (x, y) in podlocs:
                    continue

                newlocs = list(podlocs)
                newlocs[pod] = (x, y)
                new_state = State(tuple(newlocs))
                energy = get_energy(pod)
                edges.append(Edge(new_state, energy))

        return edges


def get_energy(pod):
    a = 0
    a2 = 1
    b = 2
    b2 = 3
    c = 4
    c2 = 5
    d = 6
    d2 = 7
    if pod == a or pod == a2:
        return 1
    if pod == b or pod == b2:
        return 1
    if pod == c or pod == c2:
        return 1
    if pod == d or pod == d2:
        return 1
    raise ValueError


def get_neighbors(loc):
    x, y = loc
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def is_winner(state: State):
    a = 0
    a2 = 1
    b = 2
    b2 = 3
    c = 4
    c2 = 5
    d = 6
    d2 = 7
    is_a = (state.podlocs[a] == (3, 2) and state.podlocs[a2] == (3, 3)) or (
        state.podlocs[a] == (3, 3) and state.podlocs[a2] == (3, 2)
    )
    is_b = (state.podlocs[b] == (5, 2) and state.podlocs[b2] == (5, 3)) or (
        state.podlocs[b] == (5, 3) and state.podlocs[b2] == (5, 2)
    )
    is_c = (state.podlocs[c] == (7, 2) and state.podlocs[c2] == (7, 3)) or (
        state.podlocs[c] == (7, 3) and state.podlocs[c2] == (7, 2)
    )
    is_d = (state.podlocs[d] == (9, 2) and state.podlocs[d2] == (9, 3)) or (
        state.podlocs[d] == (9, 3) and state.podlocs[d2] == (9, 2)
    )
    return is_a and is_b and is_c and is_d


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
    print(Day23.part1("/home/p22/h21/dev/aoc/2021/inputs/23/input_small3.txt"))
