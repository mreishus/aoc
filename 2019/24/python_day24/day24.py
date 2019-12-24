#!/usr/bin/env python

from collections import defaultdict, deque, Counter

# from aoc.computer import Computer
# from aoc.day23 import Day23


def grid_get_reals_imags(grid):
    """ Given a grid (dict with complex keys), get a list of all of its real
    (x) and imaginary (y) components """
    reals = [c.real for c in grid.keys()]
    imags = [c.imag for c in grid.keys()]
    return reals, imags


def generate_coords(grid):
    """ Given a grid, return a generator iterating over x, y coordinates.
    Note: Each coordinate is not guarenteed to be in the grid. """
    reals, imags = grid_get_reals_imags(grid)
    for y in range(int(min(imags)) - 0, int(max(imags)) + 1):
        for x in range(int(min(reals)) - 0, int(max(reals)) + 1):
            yield x, y


def generate_neighbors(coord):
    """ Given a coordinate (complex), return a generator iterating over its 4 direct neighbors. """
    x = int(coord.real)
    y = int(coord.imag)
    yield complex(x, y - 1)
    yield complex(x, y + 1)
    yield complex(x + 1, y)
    yield complex(x - 1, y)


class Day24:
    def __init__(self, filename):
        self.grid = None  # defaultdict(lambda: "?")
        self.parse(filename)

    def parse(self, filename):
        grid = {}
        # loc_of_door = {}
        # loc_of_key = {}
        location = complex(0, 0)

        with open(filename) as f:
            for line in f:
                for char in line.strip():
                    grid[location] = char
                    location += complex(1, 0)
                location += complex(0, 1)
                location = complex(0, location.imag)
        self.grid = grid

    def step(self):
        new_grid = {}
        for x, y in generate_coords(self.grid):
            # print(f"{x},{y}")
            char = self.grid[complex(x, y)]
            new_char = char
            adj_bugs = 0
            for neighbor in generate_neighbors(complex(x, y)):
                if neighbor in self.grid and self.grid[neighbor] == "#":
                    adj_bugs += 1
            if char == "#":
                if adj_bugs != 1:
                    new_char = "."
            elif char == ".":
                if adj_bugs == 1 or adj_bugs == 2:
                    new_char = "#"
            new_grid[complex(x, y)] = new_char
        self.grid = new_grid

    def display(self):
        reals, imags = grid_get_reals_imags(self.grid)
        for y in range(int(min(imags)) - 0, int(max(imags)) + 1):
            for x in range(int(min(reals)) - 0, int(max(reals)) + 1):
                char = self.grid[complex(x, y)]
                print(char, end="")
            print("")

    def score(self):
        n = 1
        score = 0
        for x, y in generate_coords(self.grid):
            if self.grid[complex(x, y)] == "#":
                score += n
            n *= 2
        return score

    def loop_till_dupe(self):
        seen = {}
        while True:
            a_score = self.score()
            if a_score in seen:
                return a_score
            seen[a_score] = 1
            self.step()


if __name__ == "__main__":
    d24 = Day24("../../24/input.txt")
    print(d24.loop_till_dupe())
