import pickle
import random
from copy import copy
from collections import defaultdict
from collections import deque
from aoc.computer import Computer
from os import system

COMPLEX_OF_DIR = {
    "U": complex(0, -1),
    "R": complex(1, 0),
    "D": complex(0, 1),
    "L": complex(-1, 0),
}
COMMAND_OF_DIR = {"U": 1, "R": 4, "D": 2, "L": 3}
DIRECTIONS = list(COMPLEX_OF_DIR.keys())


def roll(sides, bias_list):
    assert len(bias_list) == sides
    number = random.uniform(0, sum(bias_list))
    current = 0
    for i, bias in enumerate(bias_list):
        current += bias
        if number <= current:
            return i + 1


def possible_steps(grid, start, finish, subtree_root):
    steps = []
    for direction in DIRECTIONS:
        delta = COMPLEX_OF_DIR[direction]
        if grid[subtree_root + delta] == GRID.SPACE:
            steps.append({"child": subtree_root + delta, "action": direction})
    return steps


def construct_path(node, meta):
    actions = deque()
    while node in meta:
        node, action = meta[node]
        actions.appendleft(action)
    return actions


def bfs(grid, start, finish):
    print("Looking for")
    print(finish)
    open_set = deque()
    open_set.append(start)
    closed_set = deque()
    meta = {}
    min_rang3 = None

    while len(open_set) > 0:
        subtree_root = open_set.pop()
        # print("STR")
        # print(subtree_root)
        if is_goal(grid, start, finish, subtree_root):
            path = construct_path(subtree_root, meta)
            rang3 = len(path)
            if min_rang3 == None or rang3 < min_rang3:
                print(min_rang3)
                min_rang3 = rang3
            ## Not sure
            # if rang3 > min_rang3:
            #     continue

        # print("STEPS")
        poss = possible_steps(grid, start, finish, subtree_root)
        for step in poss:
            # print(step)
            child = step["child"]
            action = step["action"]
            if child in closed_set:
                continue
            meta[child] = [subtree_root, action]
            if child not in open_set:
                open_set.appendleft(child)

        if subtree_root not in closed_set:
            closed_set.append(subtree_root)

    return min_rang3


def is_goal(grid, start, finish, subtree_root):
    return subtree_root == finish


class RepairDroid:
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])

    def input(self, command):
        self.cpu.add_input(command)
        self.cpu.execute()
        return self.cpu.pop_output()


class GRID:
    UNK = 0
    SPACE = 1
    WALL = 2
    OXYGEN = 3


class GridMapper15:
    def __init__(self, program):
        self.rd = RepairDroid(program)
        self.grid = defaultdict(lambda: 0)
        self.location = complex(0, 0)
        self.oxygen_location = complex(0, 0)
        self.command_of_direction = {}

    def move(self, direction):
        # print(f"Moving {direction}")
        command = COMMAND_OF_DIR[direction]
        delta = COMPLEX_OF_DIR[direction]

        if self.grid[self.location + delta] == GRID.WALL:
            return

        result = self.rd.input(command)
        if result == 0:
            # Bump into wall
            self.grid[self.location + delta] = GRID.WALL
        elif result == 1:
            # Move into space
            self.location += delta
            self.grid[self.location] = GRID.SPACE
        elif result == 2:
            # Move into oxygen
            self.location += delta
            self.grid[self.location] = GRID.SPACE
            self.oxygen_location = self.location

    # Bias list: Like (0.8, 0.2, 0.1, 0.1)
    def random_move(self, bias_list):
        i = roll(4, bias_list) - 1
        direction = DIRECTIONS[i]
        self.move(direction)

    def display(self):
        reals = [c.real for c in self.grid.keys()]
        imags = [c.imag for c in self.grid.keys()]
        system("clear")
        for y in range(int(min(imags)), int(max(imags)) + 3):
            for x in range(int(min(reals)), int(max(reals)) + 3):
                char = self.grid[complex(x, y)]
                print_char = " "
                if char == GRID.SPACE:
                    print_char = " "
                elif char == GRID.WALL:
                    print_char = "#"
                elif char == GRID.UNK:
                    print_char = "."
                print(print_char, end="")
            print("")

    def explore(self):
        # for k in range(20):
        #     for j in range(25):
        #         for i in range(3000):
        #             self.random_move((0.25, 0.25, 0.25, 0.25))
        # return
        for j in range(25):
            for i in range(3000):
                self.random_move((0.50, 0.25, 0.12, 0.13))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))
            for i in range(3000):
                self.random_move((0.13, 0.50, 0.25, 0.12))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))
            for i in range(3000):
                self.random_move((0.12, 0.13, 0.50, 0.25))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))
            for i in range(3000):
                self.random_move((0.25, 0.12, 0.13, 0.50))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))

            for i in range(3000):
                self.random_move((0.50, 0.12, 0.25, 0.13))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))
            for i in range(3000):
                self.random_move((0.13, 0.50, 0.12, 0.25))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))
            for i in range(3000):
                self.random_move((0.25, 0.13, 0.50, 0.12))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))
            for i in range(3000):
                self.random_move((0.12, 0.25, 0.13, 0.50))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))

            for i in range(3000):
                self.random_move((0.50, 0.12, 0.13, 0.25))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))
            for i in range(3000):
                self.random_move((0.25, 0.50, 0.12, 0.13))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))
            for i in range(3000):
                self.random_move((0.13, 0.25, 0.50, 0.12))
            for i in range(3000):
                self.random_move((0.25, 0.25, 0.25, 0.25))
            for i in range(3000):
                self.random_move((0.12, 0.13, 0.25, 0.50))


class Day15:
    @staticmethod
    def part1(program_in):
        ## Does Random Walk to explore grid, then
        ## saves it to a pickle file (Slow, 1-2 minutes)
        gm = GridMapper15(program_in)
        gm.explore()
        mygrid = {k: v for k, v in gm.grid.items()}
        stuff = {"grid": mygrid, "oxygen_location": gm.oxygen_location}
        with open("gm_pkl", "wb") as output:
            pickle.dump(stuff, output, pickle.HIGHEST_PROTOCOL)

        ## Opens pickle file from earlier
        with open("gm_pkl", "rb") as input:
            stuff = pickle.load(input)
            gm = GridMapper15(program_in)
            for k, v in stuff["grid"].items():
                gm.grid[k] = v
            gm.oxygen_location = stuff["oxygen_location"]
            gm.display()

            a = bfs(gm.grid, complex(0, 0), gm.oxygen_location)
            print(a)

            print(Day15.part2(gm.grid, gm.oxygen_location))

    @staticmethod
    def part2(grid, oxygen_location):
        grid[oxygen_location] = GRID.OXYGEN
        minutes_passed = 0
        while True:
            grid = Day15.spread_oxygen(grid, oxygen_location)
            minutes_passed += 1
            if Day15.oxygen_fully_spread(grid):
                break
        return minutes_passed

    @staticmethod
    def spread_oxygen(grid_in, oxygen_location):
        grid = copy(grid_in)
        deltas = list(COMPLEX_OF_DIR.values())
        to_add = set()

        current_oxy = [k for k, v in grid.items() if v == GRID.OXYGEN]
        for space in current_oxy:
            for delta in deltas:
                if grid[space + delta] == GRID.SPACE:
                    to_add.add(space + delta)

        for space in to_add:
            grid[space] = GRID.OXYGEN
        return grid

    @staticmethod
    def oxygen_fully_spread(grid):
        return len([k for k, v in grid.items() if v == GRID.SPACE]) == 0
