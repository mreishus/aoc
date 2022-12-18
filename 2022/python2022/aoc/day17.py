#!/usr/bin/env python
"""
Advent Of Code 2022 Day 17
https://adventofcode.com/2022/day/17
"""
from typing import List
import numpy as np
import math
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        line = file.readlines()[0]
        return list(line.strip())


def get_shape(i):
    return {
        0: shape_line,
        1: shape_plus,
        2: shape_l,
        3: shape_i,
        4: shape_square,
    }[i % 5]()


def shape_line():
    return np.ones((1, 4), dtype=bool)


def shape_plus():
    return np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool)


def shape_square():
    return np.ones((2, 2), dtype=bool)


def shape_l():
    return np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]], dtype=bool)


def shape_i():
    return np.array([[1], [1], [1], [1]], dtype=bool)


def p1(data, iterations=2022):
    height = 64
    bottom = 64  # highest rock in the room (or ground if there isn't one)

    field = np.zeros((height, 7), dtype=bool)
    width = 7

    # print("")
    # print(np.matrix(field))
    # print(field.shape)

    piece_i = 0
    data_i = 0
    # print("Number of blocks: ", 5)
    # print("Input length: ", len(data))

    cache = defaultdict(list)
    cache2 = defaultdict(list)
    iteration = 0
    row_adj = 0
    while iteration < iterations:
        room_left = bottom
        if room_left < 7:
            # print(f"======= room left {bottom}, expanding ======")
            bottom += height
            height *= 2
            new_field = np.zeros((height, width), dtype=bool)
            new_field[field.shape[0] :, 0:] = field
            field = new_field

        top24rows = field[bottom : bottom + 24]
        shape_i = iteration % 5
        direction = data[data_i % len(data)]
        key = (top24rows.tobytes(), shape_i, direction)
        if key in cache and len(cache2[key]) >= 2:
            skip_iterations = cache[key][1] - cache[key][0]
            add_rows = cache2[key][1] - cache2[key][0]

            for multiple in [7, 6, 5, 4, 3, 2, 1]:
                factor = 10**multiple
                if iteration + (skip_iterations * factor) < iterations:
                    iteration += skip_iterations * factor
                    row_adj += add_rows * factor
                    break
        else:
            cache[key].append(iteration)
            cache2[key].append(height - bottom)

        p = get_shape(iteration)

        # Each rock appears so that its left edge is two units away from the
        # left wall and its bottom edge is three units above the highest rock
        # in the room (or the floor, if there isn't one).
        px_sz = p.shape[1]
        py_sz = p.shape[0]
        px = 2
        py = (bottom - 3) - py_sz

        stopped = False
        while not stopped:
            # Pushed by a jet
            direction = data[data_i % len(data)]
            data_i += 1
            xd = 0
            if direction == ">":
                if px + px_sz + 1 <= width:
                    if not (field[py : py + py_sz, px + 1 : px + px_sz + 1] & p).any():
                        # print("Right one")
                        xd = 1
            elif direction == "<":
                if px - 1 >= 0:
                    if not (field[py : py + py_sz, px - 1 : px + px_sz - 1] & p).any():
                        # print("Left one")
                        xd = -1
            else:
                raise Exception("Unknown direction: " + direction)
            px += xd

            # Falling one unit down
            py += 1

            # Check if it is stopped
            if py + py_sz > height:
                # print("Stop 1")
                stopped = True
            elif (field[py : py + py_sz, px : px + px_sz] & p).any():
                # print("Stop 2")
                stopped = True

            if stopped:
                py -= 1
                field[py : py + py_sz, px : px + px_sz] |= p
                bottom = min(bottom, py)
            # print("")
            # display(field)
        iteration += 1

    return (height - bottom) + row_adj


def display(a):
    for row in a:
        print("".join(["#" if x else "." for x in row]))


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


class Day17:
    """AoC 2022 Day 17"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return p1(data, 2022)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return p1(data, 10**12)
