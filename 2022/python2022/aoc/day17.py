#!/usr/bin/env python
"""
Advent Of Code 2022 Day 17
https://adventofcode.com/2022/day/17
"""
from typing import List
import heapq
import re
import numpy as np


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


def p1(data):
    height = 10
    bottom = 10  # highest rock in the room (or ground if there isn't one)

    field = np.zeros((height, 7), dtype=bool)
    # width = field.shape[1]
    width = 7

    # print("")
    # print(np.matrix(field))
    # print(field.shape)

    piece_i = 0
    data_i = 0
    for _ in range(2022):
        room_left = bottom
        # print("")
        if room_left < 7:
            # print(f"======= room left {bottom}, expanding ======")
            bottom += height
            height *= 2
            new_field = np.zeros((height, width), dtype=bool)
            new_field[field.shape[0] :, 0:] = field
            field = new_field

        p = get_shape(piece_i)
        piece_i += 1
        overlay = np.zeros((height, 7), dtype=bool)

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
            overlay[py : py + py_sz, px : px + px_sz] = np.zeros(
                (py_sz, px_sz), dtype=bool
            )
            px += xd
            overlay[py : py + py_sz, px : px + px_sz] = p

            # Falling one unit down
            overlay[py : py + py_sz, px : px + px_sz] = np.zeros(
                (py_sz, px_sz), dtype=bool
            )
            # print("Fall 1")
            py += 1
            # print("New")
            # display(field)
            # print("--")
            # display(overlay)
            # print(p)
            # print(f"px {px}, py {py} | px_sz {px_sz}, py_sz {py_sz}")
            # print(f"bottom {bottom}, height {height}, peice {piece_i}")
            # print(overlay[py : py + py_sz, px : px + px_sz])

            # Check if it is stopped
            if py + py_sz > height:
                # print("Stop 1")
                stopped = True
            elif (field[py : py + py_sz, px : px + px_sz] & p).any():
                # print("Stop 2")
                stopped = True

            if not stopped:
                overlay[py : py + py_sz, px : px + px_sz] = p

            if stopped:
                # overlay[py : py + py_sz, px : px + px_sz] = np.zeros(
                #     (py_sz, px_sz), dtype=bool
                # )
                py -= 1
                overlay[py : py + py_sz, px : px + px_sz] = p
                field |= overlay
                bottom = min(bottom, py)
            # print("")
            # display(field | overlay)

    display(field | overlay)
    print(f"The tower of blocks is {height-bottom} blocks high.")
    return height - bottom


def display(a):
    for row in a:
        print("".join(["#" if x else "." for x in row]))


class Day17:
    """AoC 2022 Day 17"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        p1(data)
        # z = shape_line()
        # print(np.matrix(z))

        # z = shape_plus()
        # print(np.matrix(z))

        # z = shape_square()
        # print(np.matrix(z))

        # z = shape_l()
        # print(np.matrix(z))

        # z = shape_i()
        # print(np.matrix(z))
        return -1

        print(data)
        if len(data) <= 20:
            print(data)
        return -1

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        if len(data) <= 20:
            print(data)
        return -2
