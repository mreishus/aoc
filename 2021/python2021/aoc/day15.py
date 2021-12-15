#!/usr/bin/env python
"""
Advent Of Code 2021 Day 15
https://adventofcode.com/2021/day/8
"""
import re
from collections import defaultdict
from queue import PriorityQueue


def parse(filename: str):
    with open(filename) as file:
        grid = {}
        y = 0
        for line in file.readlines():
            x = 0
            for char in line.strip():
                grid[x, y] = int(char)
                x += 1
            y += 1
        return grid, x, y


def get_neighbors(x, y, x_size, y_size):
    cands = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    for (xx, yy) in cands:
        if xx >= 0 and xx < x_size and yy >= 0 and yy < y_size:
            yield xx, yy


def possible_edges(loc, grid, xs, ys):
    (x, y) = loc
    r = []
    for (xx, yy) in get_neighbors(x, y, xs, ys):
        weight = grid[xx, yy]
        r.append(((xx, yy), weight))
    return r


def get_weight2(grid, xx, yy, x_size, y_size):

    x_scale = None
    if 0 <= xx and xx < x_size:
        x_scale = 0
    elif (x_size * 1) <= xx and xx < (x_size * 2):
        x_scale = 1
    elif (x_size * 2) <= xx and xx < (x_size * 3):
        x_scale = 2
    elif (x_size * 3) <= xx and xx < (x_size * 4):
        x_scale = 3
    elif (x_size * 4) <= xx and xx < (x_size * 5):
        x_scale = 4

    y_scale = None
    if 0 <= yy and yy < y_size:
        y_scale = 0
    elif (y_size * 1) <= yy and yy < (y_size * 2):
        y_scale = 1
    elif (y_size * 2) <= yy and yy < (y_size * 3):
        y_scale = 2
    elif (y_size * 3) <= yy and yy < (y_size * 4):
        y_scale = 3
    elif (y_size * 4) <= yy and yy < (y_size * 5):
        y_scale = 4

    return wrap(grid[xx % x_size, yy % y_size] + x_scale + y_scale)


def wrap(num):
    return ((num - 1) % 9) + 1


def get_neighbors2(x, y, x_size, y_size):
    cands = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    for (xx, yy) in cands:
        if xx >= 0 and xx < (x_size * 5) and yy >= 0 and yy < (y_size * 5):
            yield xx, yy


def possible_edges2(loc, grid, xs, ys):
    (x, y) = loc
    r = []
    for (xx, yy) in get_neighbors2(x, y, xs, ys):
        weight = get_weight2(grid, xx, yy, xs, ys)
        r.append(((xx, yy), weight))
    return r


class Day15:
    """ AoC 2021 Day 15 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 15 part 1 """
        grid, xs, ys = parse(filename)

        loc = (0, 0)
        goal = (xs - 1, ys - 1)

        dist_to = defaultdict(lambda: 999_999_999)
        edge_to = {}
        queue = PriorityQueue()

        loc = (0, 0)
        dist_to[loc] = 0
        queue.put((0, loc))
        while not queue.empty():
            (length, loc) = queue.get()

            # Stop searching if solution
            if loc == goal:
                break

            steps = possible_edges(loc, grid, xs, ys)
            for new_loc, length in steps:
                if dist_to[new_loc] > dist_to[loc] + length:
                    dist_to[new_loc] = dist_to[loc] + length
                    edge_to[new_loc] = loc
                    queue.put((dist_to[new_loc], new_loc))

        for k, v in dist_to.items():
            if k == goal:
                return v
        return 0

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 15 part 2 """
        grid, xs, ys = parse(filename)

        loc = (0, 0)
        goal = (5 * xs - 1, 5 * ys - 1)

        # print("--")
        # for y in range(3):
        #     for x in range(5 * xs):
        #         print(get_weight2(grid, x, y, xs, ys), end="")
        #     print("")

        dist_to = defaultdict(lambda: 999_999_999)
        edge_to = {}
        queue = PriorityQueue()

        loc = (0, 0)
        dist_to[loc] = 0
        queue.put((0, loc))
        done = set()
        while not queue.empty():
            (length, loc) = queue.get()
            # if loc in done:
            #     continue

            # Stop searching if solution
            if loc == goal:
                break

            steps = possible_edges2(loc, grid, xs, ys)
            for new_loc, length in steps:
                if dist_to[new_loc] > dist_to[loc] + length:
                    dist_to[new_loc] = dist_to[loc] + length
                    edge_to[new_loc] = loc
                    # Technically, we should check to see if new_loc
                    # is already in the Q with a higher distance and remove
                    # it?
                    # I tried adding a 'done' set to stop from processing nodes
                    # twice but it didn't seem to improve anything.
                    queue.put((dist_to[new_loc], new_loc))
            # done.add(loc)

        # print("==Done==")
        for k, v in dist_to.items():
            if k == goal:
                # print(f"{v} {k}")
                return v
        return 0
