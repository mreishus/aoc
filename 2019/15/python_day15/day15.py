#!/usr/bin/env python

from itertools import permutations
from collections import defaultdict
from os import system
import sys
import random
from collections import deque
from copy import copy
import pickle

# DEBUG = True
DEBUG = False


class OP:
    ADD = 1
    MULT = 2
    SAVE = 3
    WRITE = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    SET_REL_BASE = 9
    STOP = 99


class MODE:
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


def digit_from_right(x, n):
    return x // (10 ** n) % 10


class Computer(object):
    def __init__(self, memory, inputs):
        self.memory = defaultdict(lambda: 0)
        for i, k in enumerate(memory):
            self.memory[i] = k
        self.inputs = inputs.copy()
        self.outputs = []
        self.pc = 0
        self.state = "new"
        self.relative_base = 0

    def is_halted(self):
        return self.state == "halted"

    def direct(self, n):
        """ Get the direct value of the memory address of the Nth arg, or PC + N"""
        return self.memory[self.pc + n]

    def lookup(self, n):
        """ Get the dereferenced value of the Nth arg, after checking the Nth mode
        of the current instruction. """
        instruction = self.memory[self.pc]
        # If instruction is 105, and n=1, mode is the "1", or the 2nd digit
        # from right 0 indexed (3rd when counting naturally)
        mode = digit_from_right(instruction, n + 1)
        if mode == MODE.POSITION:
            return self.memory[self.direct(n)]
        if mode == MODE.IMMEDIATE:
            return self.direct(n)
        if mode == MODE.RELATIVE:
            # Like position, but counts from relative base
            address = self.direct(n) + self.relative_base
            return self.memory[address]
        raise Exception("Unknown mode")

    def lookup_left(self, n):
        """ Use on left side of equals only (needs better explanation) """
        instruction = self.memory[self.pc]
        mode = digit_from_right(instruction, n + 1)
        if mode == MODE.POSITION:
            return self.direct(n)
        if mode == MODE.IMMEDIATE:
            return self.direct(n)
        if mode == MODE.RELATIVE:
            return self.direct(n) + self.relative_base

    def info(self, string):
        if DEBUG:
            print(string)

    def add_input(self, x):
        self.inputs.append(x)

    def has_output(self):
        return len(self.outputs) > 0

    def pop_output(self):
        return self.outputs.pop(0)

    def execute(self):
        if self.state == "halted":
            print("Refusing to execute; is halted")
        self.state = "running"
        while True:
            instruction = self.memory[self.pc] % 100
            # print(self.memory[self.pc])
            if instruction == OP.ADD:
                self.memory[self.lookup_left(3)] = self.lookup(1) + self.lookup(2)
                self.info(
                    f"    -> ADD program[{self.direct(3)}] = {self.lookup(1)} + {self.lookup(2)} = {self.lookup(1) + self.lookup(2)}"
                )
                self.pc += 4
            elif instruction == OP.MULT:
                self.memory[self.lookup_left(3)] = self.lookup(1) * self.lookup(2)
                self.info(
                    f"    -> ADD program[{self.direct(3)}] = {self.lookup(1)} * {self.lookup(2)} = {self.lookup(1) * self.lookup(2)}"
                )
                self.pc += 4
            elif instruction == OP.SAVE:
                if len(self.inputs) == 0:
                    # print("Not enough input!")
                    self.state = "waiting_input"
                    break
                this_input = self.inputs.pop(0)

                self.memory[self.lookup_left(1)] = this_input

                self.info(
                    f"    -> SAVE program[{self.lookup(1)}] = INPUT = {this_input}"
                )
                self.pc += 2
            elif instruction == OP.WRITE:
                self.outputs.append(self.lookup(1))
                self.info(f"    -> WRITE {self.lookup(1)} = OUTPUT")
                self.pc += 2
            elif instruction == OP.JUMP_IF_TRUE:
                if self.lookup(1) != 0:
                    self.info(
                        f"    -> JUMP_IF_TRUE [{self.lookup(1)}] != 0, setting i = [{self.lookup(2)}]"
                    )
                    self.pc = self.lookup(2)
                else:
                    self.info(
                        f"    -> JUMP_IF_TRUE [{self.lookup(1)}] == 0, doing normal i+= 3"
                    )
                    self.pc += 3
            elif instruction == OP.JUMP_IF_FALSE:
                if self.lookup(1) == 0:
                    self.info(
                        f"    -> JUMP_IF_FALSE [{self.lookup(1)}] == 0, setting i = [{self.lookup(2)}]"
                    )
                    self.pc = self.lookup(2)
                else:
                    self.info(
                        f"    -> JUMP_IF_FALSE [{self.lookup(1)}] != 0, doing normal i+= 3"
                    )
                    self.pc += 3
            elif instruction == OP.LESS_THAN:
                if self.lookup(1) < self.lookup(2):
                    self.info(
                        f"    -> LESS_THAN [{self.lookup(1)}] < [{self.lookup(2)}], setting program[{self.lookup_left(3)}] = 1"
                    )
                    self.memory[self.lookup_left(3)] = 1
                else:
                    self.info(
                        f"    -> LESS_THAN [{self.lookup(1)}] not < [{self.lookup(2)}], setting program[{self.lookup_left(3)}] = 0"
                    )
                    self.memory[self.lookup_left(3)] = 0
                self.pc += 4
            elif instruction == OP.EQUALS:
                if self.lookup(1) == self.lookup(2):
                    self.info(
                        f"    -> EQUALS [{self.lookup(1)}] == [{self.lookup(2)}], setting program[{self.lookup_left(3)}] = 1"
                    )
                    self.memory[self.lookup_left(3)] = 1
                else:
                    self.info(
                        f"    -> EQUALS [{self.lookup(1)}] != [{self.lookup(2)}], setting program[{self.lookup_left(3)}] = 0"
                    )
                    self.memory[self.lookup_left(3)] = 0
                self.pc += 4
            elif instruction == OP.SET_REL_BASE:
                adj = self.lookup(1)
                self.relative_base += adj
                self.info(
                    f"    -> ADJUST RELATIVE BASE by [{adj}]. NEW BASE = [{self.relative_base}]"
                )
                self.pc += 2
            elif instruction == OP.STOP:
                self.state = "halted"
                break


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


def solve1(program_in, inputs):
    """ Given a program and inputs, make a new VM, run the program, and return
    its outputs when it stops. """
    c = Computer(program_in, inputs)
    c.execute()
    return c.outputs


def amplify_once_find_max_seq(program_in):
    """Try every combination of phase settings on the amplifiers. What is the
    highest signal that can be sent to the thrusters? (Max Val)"""
    max_val = 0
    max_sequence = []

    for seq in permutations([0, 1, 2, 3, 4]):
        phase_sequence = list(seq)
        val = amplify_once(program_in, phase_sequence)
        if val > max_val:
            max_val = val
            max_sequence = phase_sequence
    return [max_val, max_sequence]


def amplify_once(program_in, phase_sequence):
    input_signal = 0
    for setting in phase_sequence:
        outputs = solve1(program_in, [setting, input_signal])
        input_signal = outputs[0]
    return input_signal


def amplify_loop(program_in, phase_sequence):
    cpus = []
    for i in range(5):
        cpus.append(Computer(program_in, [phase_sequence[i]]))

    i = 0
    next_input = 0
    while True:
        cpus[i].add_input(next_input)
        cpus[i].execute()
        if cpus[i].state == "halted" and i == 4:
            # print("halted")
            return cpus[i].outputs[0]
        next_input = cpus[i].pop_output()
        i = (i + 1) % 5


def amplify_loop_max_seq(program_in):
    max_val = 0
    max_sequence = []
    for seq in permutations([5, 6, 7, 8, 9]):
        phase_sequence = list(seq)
        val = amplify_loop(program_in, phase_sequence)
        if val > max_val:
            max_val = val
            max_sequence = phase_sequence
    return [max_val, max_sequence]


COMPLEX_OF_DIR = {
    "U": complex(0, -1),
    "R": complex(1, 0),
    "D": complex(0, 1),
    "L": complex(-1, 0),
}


def turn_right(direction):
    return turn(direction, 1)


def turn_left(direction):
    return turn(direction, -1)


def turn(direction, n):
    directions = list(COMPLEX_OF_DIR.keys())
    new_index = (directions.index(direction) + n) % len(directions)
    return directions[new_index]


class PainterRobot(object):
    def __init__(self, program):
        self.program = program

    def run_and_return_grid(self, *, initial_color=0):
        cpu = Computer(self.program, [])
        grid = defaultdict(lambda: 0)
        location = complex(0, 0)
        direction = "U"
        grid[location] = initial_color
        # Input to program: 0 if over black (.) , 1 if over white (#)
        # Outputs two values: color to paint 0/black/. 1/white/#, then 0 = turn left, 1 = turn right
        while True:
            current_square = grid[location]
            cpu.add_input(current_square)
            cpu.execute()
            if cpu.state == "halted":
                break
            paint_color = cpu.pop_output()
            turn_dir = cpu.pop_output()
            grid[location] = paint_color
            if turn_dir == 1:
                direction = turn_right(direction)
            elif turn_dir == 0:
                direction = turn_left(direction)
            else:
                raise "Told to turn an invalid direction"
            location += COMPLEX_OF_DIR[direction]
        return grid

    @staticmethod
    def part1(program_in, *, initial_color=0):
        robot = PainterRobot(program_in)
        grid = robot.run_and_return_grid(initial_color=initial_color)
        return len(list(grid.keys()))

    @staticmethod
    def part2(program_in):
        robot = PainterRobot(program_in)
        grid = robot.run_and_return_grid(initial_color=1)
        for y in range(-3, 7):
            for x in range(-5, 45):
                value = grid[complex(x, y)]
                if value == 1:
                    print("#", end="")
                else:
                    print(" ", end="")
            print("")
        return "Look above ^"


class Breakout:
    def __init__(self, program_in):
        self.program = program_in
        self.cpu = Computer(self.program, [])
        self.grid = defaultdict(lambda: 0)

    def input(self, val):
        self.cpu.add_input(val)

    def add_quarters(self):
        self.cpu.memory[0] = 2

    def run_and_return_grid(self):
        cpu = self.cpu
        self.cpu.memory[0] = 2
        grid = self.grid

        cpu.execute()
        while cpu.has_output():
            x = cpu.pop_output()
            y = cpu.pop_output()
            what = cpu.pop_output()
            grid[complex(x, y)] = what

        return grid

    def is_halted(self):
        return self.cpu.is_halted()

    def display(self):
        system("clear")
        for y in range(25):
            for x in range(45):
                char = self.grid[complex(x, y)]
                print_char = " "
                if char == 1:
                    print_char = "W"
                elif char == 2:
                    print_char = "B"
                elif char == 3:
                    print_char = "="
                elif char == 4:
                    print_char = "*"
                print(print_char, end="")
            print("")
        print(f"Score {self.grid[complex(-1, 0)]}")

    def score(self):
        return self.grid[complex(-1, 0)]

    def get_move(self):
        grid = self.grid
        ball = list(grid.keys())[list(grid.values()).index(4)]
        ball_x = int(ball.real)
        paddle = list(grid.keys())[list(grid.values()).index(3)]
        paddle_x = int(paddle.real)
        if ball_x > paddle_x:
            return "r"
        if ball_x < paddle_x:
            return "l"
        return "."

    @staticmethod
    def part1(program_in):
        robot = Breakout(program_in)
        grid = robot.run_and_return_grid()
        return list(grid.values()).count(2)

    @staticmethod
    def part2(program_in, *, display_to_screen=False):
        robot = Breakout(program_in)
        grid = robot.run_and_return_grid()
        robot.add_quarters()
        if display_to_screen:
            robot.display()
        while True:
            a = robot.get_move()
            if a == "l":
                robot.input(-1)
            elif a == "r":
                robot.input(1)
            else:
                robot.input(0)
            if robot.is_halted():
                break
            grid = robot.run_and_return_grid()
            if display_to_screen:
                robot.display()
        return robot.score()


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


# Above
# COMPLEX_OF_DIR = {
#     "U": complex(0, -1),
#     "R": complex(1, 0),
#     "D": complex(0, 1),
#     "L": complex(-1, 0),
# }
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


# # COMPLEX_OF_DIR = {
# #     "U": complex(0, -1),
# #     "R": complex(1, 0),
# #     "D": complex(0, 1),
# #     "L": complex(-1, 0),
# # }
# COMMAND_OF_DIR = {"U": 1, "R": 4, "D": 2, "L": 3}
# DIRECTIONS = list(COMPLEX_OF_DIR.keys())
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


# class GRID:
#     UNK = 0
#     SPACE = 1
#     WALL = 2
#     OXYGEN = 3


class Day15:
    @staticmethod
    def part1(program_in):
        ## Does Random Walk to explore grid, then
        ## saves it to a pickle file (Slow, 1-2 minutes)
        #
        # gm = GridMapper15(program_in)
        # gm.explore()
        # mygrid = {k: v for k, v in gm.grid.items()}
        # stuff = {"grid": mygrid, "oxygen_location": gm.oxygen_location}
        # with open("gm_pkl", "wb") as output:
        #     pickle.dump(stuff, output, pickle.HIGHEST_PROTOCOL)

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


if __name__ == "__main__":
    program = parse("../../15/input.txt")
    print("Part 1:")
    print(Day15.part1(program))
    # print("Part 2:")
    # print(Day15.part2(program))
