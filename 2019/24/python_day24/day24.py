#!/usr/bin/env python

from collections import defaultdict, deque, Counter

# from aoc.computer import Computer
# from aoc.day23 import Day23


layer_min = -150
layer_max = 150


def grid_get_reals_imags(grid):
    """ Given a grid (dict with complex keys), get a list of all of its real
    (x) and imaginary (y) components """
    reals = [c.real for c, z in grid.keys()]
    imags = [c.imag for c, z in grid.keys()]
    return reals, imags


def generate_coords(grid):
    """ Given a grid, return a generator iterating over x, y coordinates.
    Note: Each coordinate is not guarenteed to be in the grid. """
    reals, imags = grid_get_reals_imags(grid)
    for y in range(int(min(imags)) - 0, int(max(imags)) + 1):
        for x in range(int(min(reals)) - 0, int(max(reals)) + 1):
            yield x, y


def ok_z(z):
    return layer_min <= z < layer_max


def generate_neighbors(coord, z):
    """ Given a coordinate (complex), return a generator iterating over its 4 direct neighbors. """
    x = int(coord.real)
    y = int(coord.imag)
    if x == 2 and y == 1:
        # Top row, middle column
        # Yield all but bottom
        yield complex(x, y - 1), z
        yield complex(x + 1, y), z
        yield complex(x - 1, y), z
        # Special - Yield top edge of inner
        if ok_z(z + 1):
            yield complex(0, 0), z + 1
            yield complex(1, 0), z + 1
            yield complex(2, 0), z + 1
            yield complex(3, 0), z + 1
            yield complex(4, 0), z + 1
        pass
    elif x == 3 and y == 2:
        # Middle row, right column
        # Yield all but left
        yield complex(x, y - 1), z
        yield complex(x, y + 1), z
        yield complex(x + 1, y), z
        # Special - Right edge of inner
        if ok_z(z + 1):
            yield complex(4, 0), z + 1
            yield complex(4, 1), z + 1
            yield complex(4, 2), z + 1
            yield complex(4, 3), z + 1
            yield complex(4, 4), z + 1
        pass
    elif x == 1 and y == 2:
        # Middle row, left column
        # Yield all but right
        yield complex(x, y - 1), z
        yield complex(x, y + 1), z
        yield complex(x - 1, y), z
        # Special - Left edge of inner
        if ok_z(z + 1):
            yield complex(0, 0), z + 1
            yield complex(0, 1), z + 1
            yield complex(0, 2), z + 1
            yield complex(0, 3), z + 1
            yield complex(0, 4), z + 1
        pass
    elif x == 2 and y == 3:
        # bottom row, middle column
        # Yield all but top
        yield complex(x, y + 1), z
        yield complex(x + 1, y), z
        yield complex(x - 1, y), z
        # Special - Yield bottom edge of innter
        if ok_z(z + 1):
            yield complex(0, 4), z + 1
            yield complex(1, 4), z + 1
            yield complex(2, 4), z + 1
            yield complex(3, 4), z + 1
            yield complex(4, 4), z + 1
        pass
    else:
        yield complex(x, y - 1), z
        yield complex(x, y + 1), z
        yield complex(x + 1, y), z
        yield complex(x - 1, y), z
        if ok_z(z - 1):
            if y == 0:
                # Special - "8" of outer
                yield complex(2, 1), z - 1
            if y == 4:
                # special - "18" of outer
                yield complex(2, 3), z - 1
            if x == 0:
                # Special "12" of outer
                yield complex(1, 2), z - 1
            if x == 4:
                # Special "14" of outer
                yield complex(3, 2), z - 1


class Day24:
    def __init__(self, filename):
        self.grid = None  # defaultdict(lambda: "?")
        self.parse(filename)

    def parse(self, filename):
        grid = defaultdict(lambda: ".")
        # grid = {}
        location = complex(0, 0)

        with open(filename) as f:
            for line in f:
                for char in line.strip():
                    # for z in range(layer_min, layer_max):
                    grid[location, 0] = char
                    location += complex(1, 0)
                location += complex(0, 1)
                location = complex(0, location.imag)
        self.grid = grid

    def step(self):
        new_grid = defaultdict(lambda: ".")
        for x, y in generate_coords(self.grid):
            is_center = x == 2 and y == 2
            for z in range(layer_min, layer_max):
                # print(f"{x},{y}")
                char = self.grid[complex(x, y), z]
                if is_center:
                    char = "?"
                new_char = char
                adj_bugs = 0
                # print(f"{x},{y},{z}")
                for neighbor in generate_neighbors(complex(x, y), z):
                    c_neigh, neigh_z = neighbor
                    neigh_x = int(c_neigh.real)
                    neigh_y = int(c_neigh.imag)
                    n_is_center = neigh_x == 2 and neigh_y == 2
                    if neighbor in self.grid and not n_is_center:
                        # print(f" --> {neighbor} {neigh_x} {neigh_y} {neigh_z}")
                        if neighbor in self.grid and self.grid[neighbor] == "#":
                            adj_bugs += 1
                if char == "#":
                    if adj_bugs != 1:
                        new_char = "."
                elif char == ".":
                    if adj_bugs == 1 or adj_bugs == 2:
                        new_char = "#"
                new_grid[complex(x, y), z] = new_char
        self.grid = new_grid

    def display(self, z):
        reals, imags = grid_get_reals_imags(self.grid)
        for y in range(int(min(imags)) - 0, int(max(imags)) + 1):
            for x in range(int(min(reals)) - 0, int(max(reals)) + 1):
                char = self.grid[complex(x, y), z]
                print(char, end="")
            print("")

    def num_bugs(self):
        count = 0
        for x, y in generate_coords(self.grid):
            for z in range(layer_min, layer_max):
                location = (complex(x, y), z)
                if location in self.grid and self.grid[location] == "#":
                    count += 1
        return count

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
    # d24 = Day24("../../24/input_small.txt")
    # print(d24.grid)
    print(d24.num_bugs())
    for i in range(200):
        d24.step()
    print("How many bugs present:")
    print(d24.num_bugs())
    print("--")
    d24.display(0)
    print("--")
    d24.display(1)
    print("--")
    d24.display(2)
    print("--")
    d24.display(3)
    # print(d24.loop_till_dupe())
    points = [(complex(3, 3), 0), (complex(0, 0), 0)]
    for point in points:
        print(f"Neighbors for #{point}")
        cx, z = point
        for n in generate_neighbors(cx, z):
            print(f"  {n}")
