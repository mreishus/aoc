#!/usr/bin/env python

import string
from collections import defaultdict
import networkx as nx


def parse_20(filename):
    """ Turn a filename into a grid (dict with complex keys.  values are "#",
    "." or portal names like "AB") """
    grid = {}
    with open(filename) as file:
        y = 0
        for line in file.readlines():
            x = 0
            for char in line:
                if char != " ":
                    grid[complex(x, y)] = char
                x += 1
            y += 1
    return parse_double_letters(grid)


def is_upper(letter_or_neg1):
    """ Given a character, is it an uppercase letter? """
    return letter_or_neg1 != -1 and letter_or_neg1 in string.ascii_uppercase


def is_maze(letter_or_neg1):
    """ Given a character, is it part of the maze?  It should be a # or . """
    return letter_or_neg1 != -1 and letter_or_neg1 in "#."


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
    for y in range(int(min(imags)) - 0, int(max(imags)) + 0):
        for x in range(int(min(reals)) - 0, int(max(reals)) + 0):
            yield x, y


def get_midpoints(grid):
    """ Given a grid, find the x and y midpoints """
    reals, imags = grid_get_reals_imags(grid)

    mid_y = (int(min(imags)) + int(max(imags))) // 2
    mid_x = (int(min(reals)) + int(max(reals))) // 2
    return mid_x, mid_y


def parse_double_letters(grid):
    mid_x, mid_y = get_midpoints(grid)
    outer_or_inner = {}
    for x, y in generate_coords(grid):
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

            inout = "outer" if y < mid_y else "inner"
            outer_or_inner[complex(x, y)] = inout
        # Case: Top letter of a vertical AB on a bottom edge
        if is_upper(val_d) and is_maze(val_u):
            ident = val + val_d
            del grid[complex(x, y + 1)]
            grid[complex(x, y)] = ident

            inout = "inner" if y < mid_y else "outer"
            outer_or_inner[complex(x, y)] = inout
        # Case: Right letter of a horizontal AB on a left edge
        if is_upper(val_l) and is_maze(val_r):
            ident = val_l + val
            del grid[complex(x - 1, y)]
            grid[complex(x, y)] = ident

            inout = "outer" if x < mid_x else "inner"
            outer_or_inner[complex(x, y)] = inout
        # Case: Left letter of a horizontal AB on a right edge
        if is_upper(val_r) and is_maze(val_l):
            ident = val + val_r
            del grid[complex(x + 1, y)]
            grid[complex(x, y)] = ident

            inout = "inner" if x < mid_x else "outer"
            outer_or_inner[complex(x, y)] = inout
    return grid, outer_or_inner


def find_start(grid):
    """ Find the start of the maze. (The clear spot next to the AA portal) """
    zz = next(find_spaces_for(grid, "AA"))
    return clear_space_next_to(zz, grid)


def find_end(grid):
    """ Find the end of the maze. (The clear spot next to the ZZ portal) """
    zz = next(find_spaces_for(grid, "ZZ"))
    return clear_space_next_to(zz, grid)


def find_spaces_for(grid, letters):
    """ Given a grid, and two letters like "AB", return a generator
    iterating over all coordinates that contain those letters. """
    for k, v in grid.items():
        if v == letters:
            yield k


def generate_neighbors(coord):
    """ Given a coordinate (complex), return a generator iterating over its 4 direct neighbors. """
    x = int(coord.real)
    y = int(coord.imag)
    yield complex(x, y - 1)
    yield complex(x, y + 1)
    yield complex(x + 1, y)
    yield complex(x - 1, y)


def clear_space_next_to(coord, grid):
    """ Given a grid and a coordinate to a portal, find the one clear space
    next to it. """
    for neighbor in generate_neighbors(coord):
        if grid.get(neighbor) == ".":
            return neighbor
    raise ValueError("Couldn't find clear space")


def find(f, seq):
    """ Return first item in sequence where f(item) == True. """
    for item in seq:
        if f(item):
            return item


def find_connected_portal(grid, location, portal_neighbor):
    """ Look through connections through portals.  Pass a grid, and two sets of coordinates:
    one to a clear space, the second to a neighboring portal. Returns a connected clear space
    if it can be found.
    (14, 13) = Clear space, (13, 13) = "AB" portal, (27, 27) = "AB" portal, (27, 28) = Clear space
    Example: find_connected_portal(grid, complex(14, 13), complex(13, 13)) = complex(27, 28)
    """
    portal_label = grid.get(portal_neighbor, "")
    portal_squares = find_spaces_for(grid, portal_label)
    clear_squares = [clear_space_next_to(sq, grid) for sq in portal_squares]
    not_me = find(lambda x: x != location, clear_squares)
    return not_me


def generate_graph(grid):
    G = nx.Graph()
    for x, y in generate_coords(grid):
        location = complex(x, y)
        val = grid.get(location)
        if val != ".":
            continue

        G.add_node(location)

        for neighbor in generate_neighbors(location):
            nval = grid.get(neighbor, "")
            if nval == ".":
                G.add_edge(location, neighbor)
            elif len(nval) == 2:
                connected_space = find_connected_portal(grid, location, neighbor)
                if connected_space is not None:
                    G.add_edge(location, connected_space)
    return G


def generate_recursive_graph(grid, outer_or_inner):
    G = nx.Graph()
    max_layers = 30
    for x, y in generate_coords(grid):
        location = complex(x, y)
        val = grid.get(location)
        if val != ".":
            continue

        for z in range(max_layers):
            G.add_node((location, z))

        for neighbor in generate_neighbors(location):
            nval = grid.get(neighbor, "")
            if nval == ".":  # Clear space
                for z in range(max_layers):
                    G.add_edge((location, z), (neighbor, z))
            elif len(nval) == 2:  # Portal
                inout = outer_or_inner[neighbor]
                connected_space = find_connected_portal(grid, location, neighbor)

                for z in range(max_layers):
                    # Outer portals on level 0 go nowhere
                    if z == 0 and inout == "outer":
                        continue
                    # Inner portals on max level go nowhere
                    if z == (max_layers - 1) and inout == "inner":
                        continue

                    if connected_space is not None:
                        # Outer portals go to lower levels, inner to higher
                        if inout == "outer":
                            G.add_edge((location, z), (connected_space, z - 1))
                        elif inout == "inner":
                            G.add_edge((location, z), (connected_space, z + 1))
                        else:
                            raise ValueError("Dont know if in or out")

    return G


def part1(filename):
    grid, outer_or_inner = parse_20(filename)
    G = generate_graph(grid)
    start = find_start(grid)
    end = find_end(grid)
    path = nx.shortest_path(G, start, end)
    return len(path) - 1


def part2(filename):
    grid, outer_or_inner = parse_20(filename)
    G2 = generate_recursive_graph(grid, outer_or_inner)
    start_3d = (find_start(grid), 0)
    end_3d = (find_end(grid), 0)
    path2 = nx.shortest_path(G2, start_3d, end_3d)
    return len(path2) - 1


if __name__ == "__main__":
    filename = "../../20/input.txt"
    print("Part 1: Shortest path length: ")
    print(part1(filename))
    print("Part 2: Shortest recursive path length: ")
    print(part2(filename))
