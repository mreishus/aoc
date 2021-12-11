#!/usr/bin/env python
"""
Advent Of Code 2021 Day 11
https://adventofcode.com/2021/day/11
"""


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
        (x + 1, y + 1),
        (x - 1, y + 1),
        (x + 1, y - 1),
        (x - 1, y - 1),
    ]
    for (xx, yy) in cands:
        if xx >= 0 and xx < x_size and yy >= 0 and yy < y_size:
            yield xx, yy


def step(data, xs, ys, flashes):
    for y in range(ys):
        for x in range(xs):
            data[x, y] += 1

    flashed = set()
    flash_begin = flashes
    is_all_flash = False

    def flash(xx, yy):
        nonlocal flashes
        flashed.add((xx, yy))
        flashes += 1
        for xf, yf in get_neighbors(xx, yy, xs, ys):
            data[xf, yf] += 1
            if data[xf, yf] > 9 and (xf, yf) not in flashed:
                flash(xf, yf)

    for y in range(ys):
        for x in range(xs):
            if data[x, y] > 9 and (x, y) not in flashed:
                flash(x, y)

    for (x, y) in flashed:
        data[x, y] = 0

    if flashes - flash_begin == xs * ys:
        is_all_flash = True
    return data, flashes, is_all_flash


def display(data, xs, ys):
    for y in range(ys):
        for x in range(xs):
            print(data[x, y], end="")
        print("")
    print("")


class Day11:
    """ AoC 2021 Day 11 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 11 part 1 """
        grid, xs, ys = parse(filename)
        flashes = 0
        for _ in range(100):
            grid, flashes, _ = step(grid, xs, ys, flashes)
        return flashes

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 11 part 2 """
        grid, xs, ys = parse(filename)
        flashes = 0
        for i in range(200000):
            grid, flashes, is_all_flash = step(grid, xs, ys, flashes)
            if is_all_flash:
                return i + 1
        return -1
