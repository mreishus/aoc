#!/usr/bin/env python
"""
Advent Of Code 2020 Day 11
https://adventofcode.com/2020/day/11


1000 = 8 = . Floor
0000 = 0 = L Empty
0001 = 1 = # Occupied

"""

import functools
import numpy as np


def parse(filename: str):
    with open(filename) as file:
        return np.array([parse_line(line.strip()) for line in file.readlines()])


def parse_line(line: str):
    return [0 if char == "L" else 8 for char in line]


def step(grid):
    neighbors = np.zeros(grid.shape, dtype=int)

    # Cardinal
    neighbors[1:] += grid[:-1] & 1
    neighbors[:-1] += grid[1:] & 1
    neighbors[:, 1:] += grid[:, :-1] & 1
    neighbors[:, :-1] += grid[:, 1:] & 1

    # Diagonal
    neighbors[1:, 1:] += grid[:-1, :-1] & 1
    neighbors[1:, :-1] += grid[:-1, 1:] & 1
    neighbors[:-1, 1:] += grid[1:, :-1] & 1
    neighbors[:-1, :-1] += grid[1:, 1:] & 1

    # If a seat is empty (L) and there are no occupied seats adjacent to it,
    # the seat becomes occupied.
    empty = grid == 0
    no_neighbors = neighbors == 0
    now_occupied = empty & no_neighbors

    # If a seat is occupied (#) and four or more seats adjacent to it are also
    # occupied, the seat becomes empty.
    occupied = grid & 1
    four_plus_n = neighbors >= 4

    set_empty = occupied & four_plus_n

    return (grid | now_occupied) & ~set_empty


def step2(grid):
    # print("--step--")
    neighbors = np.zeros(grid.shape, dtype=int)

    # for ix, iy in np.ndindex(a.shape):
    #     print(a[ix, iy])
    rows = grid.shape[0]  # If rows = 10, then y = 0-9 are valid
    cols = grid.shape[1]  # If cols = 10, then x = 0-9 are valid

    def valid_y(y):
        return 0 <= y < rows

    def valid_x(x):
        return 0 <= x < cols

    for y in range(0, rows):
        for x in range(0, cols):
            # print(f"Considering {x}, {y}")
            ncount = 0

            ## Right Scan
            # print("Right Scan")
            for dx in range(x + 1, cols):
                look = grid[y, dx]
                # print(f"{dx}, {y} = {look}")
                if look == 1:  # Occupied
                    ncount += 1
                    break
                elif look == 0:  # Empty
                    break

            ## Left Scan
            # print("Left Scan")
            for dx in range(x - 1, -1, -1):
                look = grid[y, dx]
                # print(f"{dx}, {y} = {look}")
                if look == 1:  # Occupied
                    ncount += 1
                    break
                elif look == 0:  # Empty
                    break

            ## Down scan
            # print("Down Scan")
            for dy in range(y + 1, rows):
                look = grid[dy, x]
                # print(f"{x} {dy} = {look}")
                if look == 1:  # Occupied
                    ncount += 1
                    break
                elif look == 0:  # Empty
                    break

            ## Up Scan
            # print("Up Scan")
            for dy in range(y - 1, -1, -1):
                look = grid[dy, x]
                # print(f"{x} {dy} =  {look}")
                if look == 1:  # Occupied
                    ncount += 1
                    break
                elif look == 0:  # Empty
                    break

            ## UpLeft Scan
            dy = y - 1
            dx = x - 1
            while valid_x(dx) and valid_y(dy):
                look = grid[dy, dx]
                if look == 1:  # Occupied
                    ncount += 1
                    break
                elif look == 0:  # Empty
                    break
                dy -= 1
                dx -= 1

            ## UpRight Scan
            # print("UpRight")
            dy = y - 1
            dx = x + 1
            while valid_x(dx) and valid_y(dy):
                look = grid[dy, dx]
                if look == 1:  # Occupied
                    ncount += 1
                    break
                elif look == 0:  # Empty
                    break
                dy -= 1
                dx += 1

            ## DownLeft Scan
            dy = y + 1
            dx = x - 1
            while valid_x(dx) and valid_y(dy):
                look = grid[dy, dx]
                if look == 1:  # Occupied
                    ncount += 1
                    break
                elif look == 0:  # Empty
                    break
                dy += 1
                dx -= 1

            ## DownRight Scan
            dy = y + 1
            dx = x + 1
            while valid_x(dx) and valid_y(dy):
                look = grid[dy, dx]
                if look == 1:  # Occupied
                    ncount += 1
                    break
                elif look == 0:  # Empty
                    break
                dy += 1
                dx += 1

            neighbors[y, x] = ncount

            # print(y, end=" ")
        # print(grid[y, x], end="")
        # print("")

    # print("--Neighbor recap (grid)--")
    # print(grid)
    # print("--Neighbor recap (neighbors)--")
    # print(neighbors)

    # If a seat is empty (L) and there are no occupied seats adjacent to it,
    # the seat becomes occupied.
    empty = grid == 0
    no_neighbors = neighbors == 0
    now_occupied = empty & no_neighbors

    # If a seat is occupied (#) and four or more seats adjacent to it are also
    # occupied, the seat becomes empty.
    occupied = grid & 1
    four_plus_n = neighbors >= 5

    set_empty = occupied & four_plus_n
    # print("Set to be empty:")
    # print(~set_empty)

    return (grid | now_occupied) & ~set_empty


def part1(grid):
    while True:
        last_grid = grid
        grid = step(grid)
        if np.array_equal(last_grid, grid):
            break
    return np.count_nonzero(grid == 1)


def part2(grid):
    # for i in range(2):
    #     grid = step2(grid)
    #     print(grid)

    # grid = step2(grid)
    # grid = step2(grid)

    while True:
        last_grid = grid
        grid = step2(grid)
        # print(grid)
        if np.array_equal(last_grid, grid):
            break
    return np.count_nonzero(grid == 1)


class Day11:
    """ AoC 2020 Day 11 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 09 part 1 """
        grid = parse(filename)
        return part1(grid)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 09 part 2 """
        grid = parse(filename)
        return part2(grid)
