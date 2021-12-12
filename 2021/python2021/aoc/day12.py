#!/usr/bin/env python
"""
Advent Of Code 2021 Day 12
https://adventofcode.com/2021/day/12
"""
from collections import defaultdict, deque
from typing import List
from dataclasses import dataclass


def parse(filename: str):
    routes = defaultdict(list)
    with open(filename) as file:
        for line in file.readlines():
            (left, right) = line.strip().split("-")
            routes[left].append(right)
            routes[right].append(left)
    return routes


def is_big(room):
    return room.isupper()


@dataclass()
class Path:
    p: List[str]
    is_small_dbl: bool


def next_states_p1(path: Path, routes):
    loc = path.p[-1]
    if loc == "end":
        return []
    for r in routes[loc]:
        if is_big(r) or r not in path.p:
            yield Path(path.p + [r], path.is_small_dbl)


def next_states_p2(path: Path, routes):
    loc = path.p[-1]
    if loc == "end":
        return []

    for r in routes[loc]:
        if r == "start":
            continue
        if is_big(r) or (path.is_small_dbl and r not in path.p):
            yield Path(path.p + [r], path.is_small_dbl)
        elif not path.is_small_dbl:
            yield Path(path.p + [r], r in path.p)


def bfs_all(routes, next_state_x):
    begin_path = Path(["start"], False)
    q = deque([begin_path])
    seen = set()
    path_count = 0

    while len(q) > 0:
        path = q.popleft()

        path_hash = "-".join(path.p)
        if path_hash in seen:
            continue
        seen.add(path_hash)

        if path.p[-1] == "end":
            path_count += 1
            continue

        for next_path in next_state_x(path, routes):
            q.append(next_path)

    return path_count


class Day12:
    """ AoC 2021 Day 12 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 12 part 1 """
        routes = parse(filename)
        return bfs_all(routes, next_states_p1)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 12 part 2 """
        routes = parse(filename)
        return bfs_all(routes, next_states_p2)
