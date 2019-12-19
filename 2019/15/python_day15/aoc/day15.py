import copy
from collections import defaultdict
from collections import deque
from aoc.computer import Computer

COMPLEX_OF_DIR = {
    "U": complex(0, -1),
    "R": complex(1, 0),
    "D": complex(0, 1),
    "L": complex(-1, 0),
}
COMMAND_OF_DIR = {"U": 1, "R": 4, "D": 2, "L": 3}
DIRECTIONS = list(COMPLEX_OF_DIR.keys())


def possible_steps(grid, here):
    for direction in DIRECTIONS:
        delta = COMPLEX_OF_DIR[direction]
        if grid[here + delta] == GRID.SPACE:
            yield {"child": here + delta, "action": direction}


def construct_path(node, meta):
    actions = deque()
    while node in meta:
        node, action = meta[node]
        actions.appendleft(action)
    return actions


def bfs(grid, start, finish):
    open_set = deque()
    open_set.append(start)
    closed_set = deque()
    meta = {}
    min_range = 1e6

    while len(open_set) > 0:
        here = open_set.pop()
        if here == finish:
            path = construct_path(here, meta)
            a_range = len(path)
            if a_range < min_range:
                min_range = a_range
            if a_range > min_range:
                continue

        for step in possible_steps(grid, here):
            child = step["child"]
            action = step["action"]
            if child in closed_set:
                continue
            meta[child] = [here, action]
            if child not in open_set:
                open_set.appendleft(child)

        if here not in closed_set:
            closed_set.append(here)

    return min_range


class RepairDroid:
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])

    def input(self, command):
        self.cpu.add_input(command)
        self.cpu.execute()
        return self.cpu.pop_output()

    def get_state(self):
        return copy.copy(self.cpu.memory)

    def set_state(self, state):
        self.cpu.memory = copy.copy(state)


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

    def move_peek(self, direction):
        """ Move in the direction and return what's there, but
        reset the bot state after """
        loc = copy.copy(self.location)
        state = self.rd.get_state()
        answer = self.move(direction)
        self.rd.set_state(state)
        self.location = loc
        return answer

    def move(self, direction):
        """ Move in the direction, record and return what's there
        Bot state is updated """
        command = COMMAND_OF_DIR[direction]
        delta = COMPLEX_OF_DIR[direction]

        if self.grid[self.location + delta] == GRID.WALL:
            return GRID.WALL

        result = self.rd.input(command)
        if result == 0:
            # Bump into wall
            self.grid[self.location + delta] = GRID.WALL
            return GRID.WALL
        if result == 1:
            # Move into space
            self.location += delta
            self.grid[self.location] = GRID.SPACE
            return GRID.SPACE
        if result == 2:
            # Move into oxygen
            self.location += delta
            self.grid[self.location] = GRID.SPACE
            self.oxygen_location = self.location
            return GRID.SPACE

        raise ValueError("Didn't understand response from intcode after moving")
        return GRID.SPACE

    def display(self):
        """ Display the current known grid to screen. """
        reals = [c.real for c in self.grid.keys() if self.grid[c] != GRID.UNK]
        imags = [c.imag for c in self.grid.keys() if self.grid[c] != GRID.UNK]
        # system("clear")
        for y in range(int(min(imags)) - 2, int(max(imags)) + 3):
            for x in range(int(min(reals)) - 2, int(max(reals)) + 3):
                char = self.grid[complex(x, y)]
                print_char = " "
                if self.location == complex(x, y):
                    print_char = "R"
                elif char == GRID.SPACE:
                    print_char = " "
                elif char == GRID.WALL:
                    print_char = "#"
                elif char == GRID.UNK:
                    print_char = "."
                print(print_char, end="")
            print("")

    def explore(self):
        # key: coordinate (complex) value: boolean (Have we visited it?)
        self.visited = {}
        self.path_to = {}
        self.state_for_coord = {}
        self.source = self.location  # (0, 0)
        self.explore_dfs(self.source)

    def explore_dfs(self, coord):
        if coord != self.location:
            raise ValueError("What")
        self.visited[coord] = True
        self.state_for_coord[coord] = self.rd.get_state()

        for direction in reversed(DIRECTIONS):
            # Have we been there before?
            new_coord = coord + COMPLEX_OF_DIR[direction]
            if new_coord in self.visited:
                continue

            # Load state, actually move bot and recurse
            self.rd.set_state(self.state_for_coord[coord])
            self.location = coord

            # Is it a wall?
            whats_there = self.move_peek(direction)
            if whats_there == GRID.WALL:
                continue

            # Mark path, Move there and recurse
            self.path_to[new_coord] = coord
            self.move(direction)
            self.explore_dfs(new_coord)


class Day15:
    @staticmethod
    def part1_and_2(program_in):
        gm = GridMapper15(program_in)
        gm.explore()
        p1 = bfs(gm.grid, complex(0, 0), gm.oxygen_location)
        p2 = Day15.part2_from_gm(gm)
        return p1, p2

    @staticmethod
    def part2_from_gm(gm):
        grid = gm.grid
        oxygen_location = gm.oxygen_location

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
        grid = copy.copy(grid_in)
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
