#!/usr/bin/env python

from collections import defaultdict, deque, Counter
from aoc.computer import Computer
from aoc.day23 import Day23
import copy
import re


class Day25:
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])
        self.location = complex(0, 0)

    def get_state(self):
        return copy.copy(self.cpu.memory)

    def set_state(self, state):
        self.cpu.memory = copy.copy(state)

    def execute_silent(self):
        """ Execute CPU and return results as array. """
        self.cpu.execute()
        result = []
        while self.cpu.has_output():
            result.append(self.cpu.pop_output())
        return result

    def execute_str(self):
        """ Execute CPU and return results as str. """
        result = self.execute_silent()
        return self.num_to_str(result)

    def send_msg(self, string):
        print(f"> {string}")
        nums = self.string_to_nums(string + "\n")
        for i in nums:
            self.cpu.add_input(i)

    def explore(self):
        self.visited = {}
        self.visited[complex(-3, 1)] = True
        self.path_to = {}
        self.state_for_coord = {}
        self.location_of_item = {}
        self.source = self.location  # (0, 0)

        # Debug: Move
        # self.execute_silent()
        # self.send_msg("north")

        self.explore_dfs(self.source)

        print(self.path_to)
        print(self.location_of_item)

    def explore_dfs(self, coord):
        """ This is broken because the game doesn't follow a grid;
        the arcade overlaps with the Holodeck.  Should change
        coordintes/paths to use room names instead of coordinates """
        if coord != self.location:
            raise ValueError("What")

        # Execute / Print message to screen
        message = self.execute_str()
        print(f"===ExploreDFS [{self.location}]")
        print(message)

        # Mark as visited and save state
        self.visited[coord] = True
        self.state_for_coord[coord] = self.get_state()

        # Record items here
        items = self.parse_items(message)
        for item in items:
            self.location_of_item[item] = self.location

        directions = self.parse_directions(message)
        for (command, delta) in directions:
            # Have we been there before?
            new_coord = coord + delta
            if new_coord in self.visited:
                continue

            # Load state
            self.set_state(self.state_for_coord[coord])
            self.location = coord

            # Mark path, Move there and recurse
            self.path_to[new_coord] = coord

            # (move)
            self.send_msg(command)
            self.location += delta

            self.explore_dfs(new_coord)

    def move(self, command, delta):
        pass

    # in: message
    # out: [('north', -1j), ('south', 1j), ('west', (-1+0j))]
    def parse_directions(self, message):
        dirs = []
        if re.search(r"- east", message):
            dirs.append(("east", complex(1, 0)))
        if re.search(r"- north", message):
            dirs.append(("north", complex(0, -1)))
        if re.search(r"- south", message):
            dirs.append(("south", complex(0, 1)))
        if re.search(r"- west", message):
            dirs.append(("west", complex(-1, 0)))
        return dirs

    # in: message
    # out: [] or ['tambourine']
    def parse_items(self, message):
        return re.findall(f"Items here:(?:\n- (.+))+", message)

    def part1(self):
        # self.explore()
        while True:
            print(self.execute_str())
            ins = input("command> ")
            if ins == "w":
                ins = "west"
            elif ins == "e":
                ins = "east"
            elif ins == "n":
                ins = "north"
            elif ins == "s":
                ins = "south"
            self.send_msg(ins)
        return 5

    def num_to_str(self, results):
        return "".join([chr(s) for s in results])

    def string_to_nums(self, string):
        return [ord(s) for s in string]

    def part2(self):
        return 6


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


if __name__ == "__main__":
    program = parse("../../25/input.txt")
    d25 = Day25(program)

    p1 = d25.part1()
    print("part 1")
    print(p1)

    p2 = d25.part2()
    print("part 2")
    print(p2)
