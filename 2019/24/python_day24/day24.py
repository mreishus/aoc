#!/usr/bin/env python

from collections import defaultdict


def gen_coords():
    for y in range(5):
        for x in range(5):
            yield x, y


def in_bounds(coord):
    x = int(coord.real)
    y = int(coord.imag)
    return 0 <= x <= 4 and 0 <= y <= 4


def gen_2d_neighbors(coord):
    x = int(coord.real)
    y = int(coord.imag)
    candidates = [
        complex(x, y - 1),
        complex(x, y + 1),
        complex(x + 1, y),
        complex(x - 1, y),
    ]

    for coord in candidates:
        if in_bounds(coord):
            yield coord


def gen_3d_neighbors(coord, z):
    for this_coord, this_z in gen_3d_neighbors_raw(coord, z):
        if this_coord != complex(2, 2) and in_bounds(this_coord):
            yield this_coord, this_z


def gen_3d_neighbors_raw(coord, z):
    """ Given a coordinate (complex), return a generator iterating over its 4 direct neighbors. """
    x = int(coord.real)
    y = int(coord.imag)

    yield complex(x, y - 1), z
    yield complex(x, y + 1), z
    yield complex(x + 1, y), z
    yield complex(x - 1, y), z

    if x == 2 and y == 1:
        # Top row, middle column
        # Special - Yield top edge of inner
        for inner_x in range(5):
            yield complex(inner_x, 0), z + 1
    elif x == 3 and y == 2:
        # Middle row, right column
        # Special - Right edge of inner
        for inner_y in range(5):
            yield complex(4, inner_y), z + 1
    elif x == 1 and y == 2:
        # Middle row, left column
        # Special - Left edge of inner
        for inner_y in range(5):
            yield complex(0, inner_y), z + 1
    elif x == 2 and y == 3:
        # bottom row, middle column
        # Special - Yield bottom edge of innter
        for inner_x in range(5):
            yield complex(inner_x, 4), z + 1
    else:
        if y == 0:
            # Special - "8" of outer (See problem diagram)
            yield complex(2, 1), z - 1
        if y == 4:
            # special - "18" of outer
            yield complex(2, 3), z - 1
        if x == 0:
            # Special - "12" of outer
            yield complex(1, 2), z - 1
        if x == 4:
            # Special - "14" of outer
            yield complex(3, 2), z - 1


class Day24:
    def __init__(self, filename):
        self.filename = filename
        self.reset()

    def reset(self):
        self.grid = None  # defaultdict(lambda: "?")
        self.parse(self.filename)
        self.current_layer_min = -2
        self.current_layer_max = 2

    def parse(self, filename):
        grid = defaultdict(lambda: ".")
        location = complex(0, 0)

        with open(filename) as f:
            for line in f:
                for char in line.strip():
                    grid[location, 0] = char
                    location += complex(1, 0)
                location += complex(0, 1)
                location = complex(0, location.imag)
        self.grid = grid

    def step_3d(self):
        new_grid = defaultdict(lambda: ".")
        for x, y in gen_coords():
            is_center = x == 2 and y == 2
            if is_center:
                continue
            for z in range(self.current_layer_min, self.current_layer_max):
                char = self.grid[complex(x, y), z]

                adj_bugs = sum(
                    1 for n in gen_3d_neighbors(complex(x, y), z) if self.grid[n] == "#"
                )

                new_char = char
                if char == "#" and adj_bugs != 1:
                    new_char = "."
                elif char == "." and (adj_bugs in [1, 2]):
                    new_char = "#"
                new_grid[complex(x, y), z] = new_char
        self.grid = new_grid
        self.current_layer_max += 1
        self.current_layer_min -= 1

    def step_2d(self):
        new_grid = defaultdict(lambda: ".")
        z = 0
        for x, y in gen_coords():
            char = self.grid[complex(x, y), z]

            adj_bugs = sum(
                1 for n in gen_2d_neighbors(complex(x, y)) if self.grid[n, z] == "#"
            )

            new_char = char
            if char == "#" and adj_bugs != 1:
                new_char = "."
            elif char == "." and (adj_bugs in [1, 2]):
                new_char = "#"
            new_grid[complex(x, y), z] = new_char
        self.grid = new_grid

    def display(self, z):
        for y in range(5):
            for x in range(5):
                char = self.grid[complex(x, y), z]
                print(char, end="")
            print("")

    def num_bugs(self):
        count = 0
        for x, y in gen_coords():
            for z in range(self.current_layer_min, self.current_layer_max):
                location = (complex(x, y), z)
                if location in self.grid and self.grid[location] == "#":
                    count += 1
        return count

    def score_2d(self):
        z = 0
        n = 1
        score = 0
        for x, y in gen_coords():
            if self.grid[complex(x, y), z] == "#":
                score += n
            n *= 2
        return score

    def loop_till_dupe(self):
        seen = {}
        while True:
            a_score = self.score_2d()
            if a_score in seen:
                return a_score
            seen[a_score] = 1
            self.step_2d()

    def part1(self):
        self.reset()
        return self.loop_till_dupe()

    def part2(self, num_steps=200):
        self.reset()
        for _ in range(num_steps):
            self.step_3d()
        return self.num_bugs()


if __name__ == "__main__":
    d24 = Day24("../../24/input.txt")
    print("Part 1, first repeating biodiversity score [2d]:")
    print(d24.part1())

    print("Part 2, how many bugs present, after 200 steps [3d, recursive]:")
    print(d24.part2())
