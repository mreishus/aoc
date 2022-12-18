#!/usr/bin/env python
"""
Advent Of Code 2022 Day 18
https://adventofcode.com/2022/day/18


TODO: Rewrite to only do one BFS/flood fill
"""
import re
import numpy as np
from functools import cache


def ints(s: str):
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def parse(filename: str):
    with open(filename) as file:
        return [ints(line.strip()) for line in file.readlines()]


@cache
def get_neighbors(x, y, z):
    r = []
    for dx in (-1, 1):
        r.append((x + dx, y, z))
    for dy in (-1, 1):
        r.append((x, y + dy, z))
    for dz in (-1, 1):
        r.append((x, y, z + dz))
    return r


def p1(data):
    seen = set()
    for x, y, z in data:
        seen.add((x, y, z))

    edge_count = 0
    for x, y, z in data:
        for x2, y2, z2 in get_neighbors(x, y, z):
            if (x2, y2, z2) not in seen:
                # print("Edge: ", x, y, z, "| ", x2, y2, z2)
                edge_count += 1
    return edge_count


class Cube:
    def __init__(self, data):
        self.data = data
        self.calculate_seen()
        self.calculate_max()
        self.goals = set()
        self.goals.add((0, 0, 0))
        self.goals.add((self.max_x, self.max_y, self.max_z))
        self.goals.add((0, self.max_y, self.max_z))
        self.goals.add((self.max_x, 0, self.max_z))
        self.goals.add((self.max_x, self.max_y, 0))

    def calculate_seen(self):
        seen = set()
        for x, y, z in self.data:
            seen.add((x, y, z))
        self.blocks = seen

    def calculate_max(self):
        self.max_x = max(x for x, _, _ in self.data)
        self.max_y = max(y for _, y, _ in self.data)
        self.max_z = max(z for _, _, z in self.data)

    @cache
    def get_empty_neighbors(self, x, y, z):
        r = []
        for x2, y2, z2 in get_neighbors(x, y, z):
            if (x2, y2, z2) not in self.blocks:
                r.append((x2, y2, z2))
        return r

    @cache
    def bfs(self, x, y, z):
        seen = set()
        queue = [(x, y, z)]
        came_from = {}

        while queue:
            x, y, z = queue.pop(0)
            if (x, y, z) in seen:
                continue
            seen.add((x, y, z))

            if (x, y, z) in self.goals:
                if (x, y, z) in came_from:
                    self.goals.add(came_from[(x, y, z)])
                return True

            for x2, y2, z2 in self.get_empty_neighbors(x, y, z):
                queue.append((x2, y2, z2))
                came_from[(x2, y2, z2)] = (x, y, z)

        return False


def p2(data):
    c = Cube(data)

    edge_count = 0
    for x, y, z in c.data:
        for x2, y2, z2 in get_neighbors(x, y, z):
            if (x2, y2, z2) not in c.blocks:
                reachable = c.bfs(x2, y2, z2)
                # print("Edge: ", x, y, z, "| ", x2, y2, z2, "||", reachable)
                if reachable:
                    edge_count += 1
    return edge_count


class Day18:
    """AoC 2022 Day 18"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        return p2(data)
