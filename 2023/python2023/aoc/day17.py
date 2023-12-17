#!/usr/bin/env python
"""
Advent Of Code 2023 Day 17
https://adventofcode.com/2023/day/17
"""
from typing import List
from collections import defaultdict, namedtuple
from aoc.heapdict import heapdict

State = namedtuple("State", ("loc", "direction", "streak"))
Move = namedtuple("Move", ("state", "distance"))


class Grid:
    def __init__(self):
        self.grid = {}
        self.is_lit = defaultdict(bool)
        self.max_x = 0
        self.max_y = 0

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[(x, y)] = char
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                print(self.grid[(x, y)], end="")
            print()

    def display2(self, path):
        path_dict = {state.loc: state.direction for state in path}
        print("")

        direction_arrows = {"E": ">", "W": "<", "N": "^", "S": "v", "": "•"}

        for y in range(self.max_y):
            for x in range(self.max_x):
                loc = (x, y)
                if loc in path_dict:
                    print(direction_arrows[path_dict[loc]], end="")
                else:
                    print(" ", end="")
                    # print(self.grid[loc], end="")
            print()

    def pathfind(self):
        """
        State = namedtuple("State", ("loc", "direction", "streak"))
        Move = namedtuple("Move", ("state", "distance"))
        """
        loc_start = (0, 0)
        loc_end = (self.max_x - 1, self.max_y - 1)

        state_start = State(loc_start, "", 0)

        dist_to = defaultdict(lambda: 999_999_999_999_999_999_999_999)
        edge_to = {}
        open_set = heapdict()

        dist_to[state_start] = 0
        open_set[state_start] = 0
        while len(open_set) > 0:
            (state, length) = open_set.popitem()

            if state.loc == loc_end:
                return length, self.reconstruct_path(edge_to, state_start, state)

            moves = self.available_moves(state)
            # print("first try")
            # print("state", state)
            # print("moves", moves)

            for move in moves:
                new_state = move.state
                if dist_to[new_state] > dist_to[state] + move.distance:
                    dist_to[new_state] = dist_to[state] + move.distance
                    edge_to[new_state] = state
                    open_set[new_state] = dist_to[new_state]

    def reconstruct_path(self, edge_to, start_state, end_state):
        path = []
        current_state = end_state
        while current_state != start_state:
            current_state = edge_to[current_state]
            path.append(current_state)
        path.reverse()
        return path

    def available_moves(self, state: State) -> List[Move]:
        loc = state.loc
        old_direction = state.direction

        moves = []
        opposites = {"N": "S", "S": "N", "E": "W", "W": "E"}
        for direction in ["N", "S", "E", "W"]:
            if direction == opposites.get(old_direction):
                continue

            x, y = self.move(loc, direction)
            if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
                continue

            distance = int(self.grid[(x, y)])

            streak = 1
            if old_direction == direction:
                streak = state.streak + 1
            if streak > 3:
                continue

            new_state = State((x, y), direction, streak)
            moves.append(Move(new_state, distance))

        return moves

    def move(self, loc: tuple, direction: str) -> tuple:
        x = loc[0]
        y = loc[1]

        if direction == "N":
            y -= 1
        elif direction == "S":
            y += 1
        elif direction == "E":
            x += 1
        elif direction == "W":
            x -= 1
        else:
            raise ValueError(f"Invalid direction: {direction}")

        return (x, y)


class Day17:
    """AoC 2023 Day 17"""

    @staticmethod
    def part1(filename: str) -> int:
        """
        Incorrect gguesses: 692
        """
        g = Grid()
        g.parse(filename)
        length, path = g.pathfind()
        # g.display2(path)
        return length

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        print(data)
        return -1
