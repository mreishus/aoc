#!/usr/bin/env python

import string
import networkx as nx
from collections import defaultdict
from aoc.computer import Computer, solve1
from aoc.day19 import Day19


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


def parse_20(filename):
    grid = {}
    with open(filename) as file:
        y = 0
        for line in file.readlines():
            print(line)
            x = 0
            for char in line:
                if char != " ":
                    grid[complex(x, y)] = char
                x += 1
            y += 1
    return parse_double_letters(grid)


def is_upper(letter_or_neg1):
    if letter_or_neg1 == -1:
        return False
    return letter_or_neg1 in string.ascii_uppercase


def is_maze(letter_or_neg1):
    if letter_or_neg1 == -1:
        return False
    return letter_or_neg1 in "#."


def parse_double_letters(grid):
    reals = [c.real for c in grid.keys() if grid[c] != "q"]
    imags = [c.imag for c in grid.keys() if grid[c] != "q"]
    for y in range(int(min(imags)) - 0, int(max(imags)) + 0):
        for x in range(int(min(reals)) - 0, int(max(reals)) + 0):
            val = grid.get(complex(x, y), -1)
            if not is_upper(val):
                continue
            val_r = grid.get(complex(x + 1, y), -1)
            val_l = grid.get(complex(x - 1, y), -1)
            val_u = grid.get(complex(x, y - 1), -1)
            val_d = grid.get(complex(x, y + 1), -1)
            # Case: Bottom letter of a vertical AB on a top edge
            if is_upper(val_u) and is_maze(val_d):
                ident = val_u + val
                del grid[complex(x, y - 1)]
                grid[complex(x, y)] = ident
            # Case: Top letter of a vertical AB on a bottom edge
            if is_upper(val_d) and is_maze(val_u):
                ident = val + val_d
                del grid[complex(x, y + 1)]
                grid[complex(x, y)] = ident
            # Case: Right letter of a horizontal AB on a left edge
            if is_upper(val_l) and is_maze(val_r):
                ident = val_l + val
                del grid[complex(x - 1, y)]
                grid[complex(x, y)] = ident
            # Case: Left letter of a horizontal AB on a right edge
            if is_upper(val_r) and is_maze(val_l):
                ident = val + val_r
                del grid[complex(x + 1, y)]
                grid[complex(x, y)] = ident
    return grid


def find_start(grid):
    zz = next(find_spaces_for(grid, "AA"))
    return clear_space_next_to(zz, grid)


def find_end(grid):
    zz = next(find_spaces_for(grid, "ZZ"))
    return clear_space_next_to(zz, grid)


def find_spaces_for(grid, letters):
    for k, v in grid.items():
        if v == letters:
            yield k


def clear_space_next_to(coord, grid):
    x = int(coord.real)
    y = int(coord.imag)
    up = complex(x, y - 1)
    down = complex(x, y + 1)
    right = complex(x + 1, y)
    left = complex(x - 1, y)
    if grid.get(up) == ".":
        return up
    if grid.get(down) == ".":
        return down
    if grid.get(right) == ".":
        return right
    if grid.get(left) == ".":
        return left
    raise ValueError("Couldn't find clear space")
    return coord


def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item):
            return item


def generate_graph(grid):
    G = nx.Graph()
    reals = [c.real for c in grid.keys() if grid[c] != "q"]
    imags = [c.imag for c in grid.keys() if grid[c] != "q"]
    for y in range(int(min(imags)) - 0, int(max(imags)) + 0):
        for x in range(int(min(reals)) - 0, int(max(reals)) + 0):
            location = complex(x, y)
            val = grid.get(location)
            if val != ".":
                continue

            G.add_node(location)

            up = location + complex(0, -1)
            down = location + complex(0, 1)
            left = location + complex(-1, 0)
            right = location + complex(1, 0)

            for neighbor in [up, down, left, right]:
                nval = grid.get(neighbor, "")
                if nval == ".":
                    G.add_edge(location, neighbor)
                elif len(nval) == 2:
                    portal_squares = find_spaces_for(grid, nval)
                    clear_squares = [
                        clear_space_next_to(sq, grid) for sq in portal_squares
                    ]
                    not_me = find(lambda x: x != location, clear_squares)
                    if not_me is not None:
                        G.add_edge(location, not_me)

                    # print(f"Need to add edge for portal [{nval}]")
                    # print(
                    #     f"Loc {location} Neighbor {neighbor} Clear Squares {clear_squares}"
                    # )
                    # print(f"Not me {not_me}")
    return G


if __name__ == "__main__":
    print("Main")
    # grid = parse_20("../../20/input_23.txt")
    # grid = parse_20("../../20/input_58.txt")
    grid = parse_20("../../20/input.txt")
    print(grid)
    start = find_start(grid)
    end = find_end(grid)
    print(list(find_spaces_for(grid, "BC")))
    G = generate_graph(grid)
    path = nx.dijkstra_path(G, start, end)
    print(path)
    print("Shortest path length: ")
    print(len(path) - 1)
    # program = parse("../../20/input.txt")
    # d9 = Day19(program)
    # print("Part1")
    # print(d9.part1())
    # print("Part2")
    # print(d9.part2())
