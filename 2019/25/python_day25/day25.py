#!/usr/bin/env python

from collections import defaultdict, deque, Counter
from aoc.computer import Computer
from aoc.day23 import Day23
from itertools import combinations
import networkx as nx
import copy
import re


class Day25:
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])

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

    def opposite_dir(self, direction):
        opposites = {"west": "east", "east": "west", "south": "north", "north": "south"}
        if direction in opposites:
            return opposites[direction]
        raise ValueError(f"Don't know opposite of [{direction}]")

    def explore(self):
        self.cpu = Computer(self.program, [])
        self.loc = None
        # visited[ 'Hull Breach'] = true
        # dir_from_to[ ('Hull Breach', 'Holodeck') ] = 'north'
        # Possibly Delete: dirs_for_loc['Hull Breach'] = ['north', 'west', 'south']
        # state_for_loc['Hull Breach'] = (memory state for int comp)
        # loc_of_item['tambourine'] = 'Holodeck'
        # G = (networkx graph)
        self.visited = {}
        self.dir_from_to = {}
        self.dirs_for_loc = {}
        self.state_for_loc = {}
        self.loc_of_item = {}
        self.G = nx.Graph()

        self.explore_dfs(None, None)

    def explore_dfs(self, command_used, came_from):
        # Execute, read text and get room name
        message = self.execute_str()
        room_name = self.parse_title(message)
        loc = room_name
        self.loc = loc
        print(f"=== ExploreDFS [{loc}] ===")

        # Save the way we got here
        if command_used is not None and came_from is not None:
            self.G.add_edge(came_from, loc)
            self.dir_from_to[(came_from, loc)] = command_used
            self.dir_from_to[(loc, came_from)] = self.opposite_dir(command_used)

        # Been here before?
        if loc in self.visited:
            return

        # Mark as visited and save state
        self.visited[loc] = True
        self.state_for_loc[loc] = self.get_state()

        # Record items here
        for item in self.parse_items(message):
            self.loc_of_item[item] = loc

        directions = self.parse_directions(message)
        self.dirs_for_loc[loc] = directions

        for command in directions:
            # Load state
            self.set_state(self.state_for_loc[loc])

            # Move and recurse
            self.send_msg(command)
            self.explore_dfs(command_used=command, came_from=loc)

    def pick_up_items(self):
        print("=== Picking up all items")
        # Reset computer
        self.cpu = Computer(self.program, [])
        message = self.execute_str()
        loc = self.parse_title(message)

        for item in self.loc_of_item:
            if self.is_blacklisted(item):
                continue
            destination = self.loc_of_item[item]
            self.move(loc, destination)
            loc = destination
            self.loc = loc
            self.send_msg(f"take {item}")
            message = self.execute_str()

    def move(self, loc, destination):
        path = nx.shortest_path(self.G, loc, destination)
        path.pop(0)  # First item in path is always where we are
        while len(path) > 0:
            next_loc = path.pop(0)
            direction = self.dir_from_to[(loc, next_loc)]
            self.send_msg(direction)
            message = self.execute_str()
            room_name = self.parse_title(message)
            assert room_name == next_loc
            loc = next_loc
            self.loc = loc

    def try_all_items(self):
        print("=== Going to Security Checkpoint")
        destination = "Security Checkpoint"
        self.move(self.loc, destination)
        items = self.get_items()

        for item in items:
            self.send_msg(f"drop {item}")

        for n in range(len(items)):
            for these_items in list(combinations(items, n)):
                for item in these_items:
                    self.send_msg(f"take {item}")
                self.send_msg("south")

                message = self.execute_str()
                if self.cpu.is_halted():
                    print("")
                    print(f"Correct combination: {these_items}")
                    print("")
                    print(message)
                    return

                for item in these_items:
                    self.send_msg(f"drop {item}")

    def get_items(self):
        self.send_msg("inv")
        message = self.execute_str()
        items = self.parse_list(message)
        return items

    def is_blacklisted(self, item):
        return item in [
            "infinite loop",
            "escape pod",
            "molten lava",
            "giant electromagnet",
            "photons",
        ]

    # in: message
    # out: ["north", "east", "west"]
    def parse_directions(self, message):
        dirs = []
        if re.search(r"- east\n", message):
            dirs.append("east")
        if re.search(r"- north\n", message):
            dirs.append("north")
        if re.search(r"- south\n", message):
            dirs.append("south")
        if re.search(r"- west\n", message):
            dirs.append("west")
        return dirs

    # in: message
    # out: [] or ['tambourine']
    def parse_list(self, message):
        return re.findall(r"- (.*?)(?:\n|$)", message)

    def parse_items(self, message):
        item_list = re.findall("Items (?:here|in your inventory):\n(.*)\n\n", message)
        if len(item_list) > 0:
            return self.parse_list(item_list[0])
        return []

    # in: message
    # out: "Hull Breach"
    def parse_title(self, message):
        titles = re.findall(f"== (.*?) ==", message)
        if len(titles) < 1:
            raise ValueError("Couldn't find title of this room")
        return titles[0]

    def part1(self):
        while True:
            print(self.execute_str())
            ins = input(
                "command (w, n, e, s, take item, drop item, or 'solve' to automatically solve)> "
            )
            if ins == "w":
                ins = "west"
            elif ins == "e":
                ins = "east"
            elif ins == "n":
                ins = "north"
            elif ins == "s":
                ins = "south"
            elif ins == "solve":
                self.explore()
                self.pick_up_items()
                self.try_all_items()
                return
            self.send_msg(ins)
        return None

    def num_to_str(self, results):
        return "".join([chr(s) for s in results])

    def string_to_nums(self, string):
        return [ord(s) for s in string]


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


if __name__ == "__main__":
    program = parse("../../25/input.txt")
    d25 = Day25(program)

    d25.part1()
