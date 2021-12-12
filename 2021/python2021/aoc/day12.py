#!/usr/bin/env python
"""
Advent Of Code 2021 Day 12
https://adventofcode.com/2021/day/12
"""
from collections import defaultdict, Counter, deque
from typing import List


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


class Path:
    def __init__(self, path_list: List[str], is_small_double: bool):
        self.p = path_list
        self.is_small_double = is_small_double


def next_states_p1(path: Path, routes):
    loc = path.p[-1]
    if loc == "end":
        return []
    return [r for r in routes[loc] if is_big(r) or r not in path.p]


def next_states_p2(path: Path, routes):
    loc = path.p[-1]
    if loc == "end":
        return []

    for r in routes[loc]:
        if r == "start":
            continue
        if is_big(r):
            yield r
        elif path.is_small_double and r not in path.p:
            yield r
        elif not path.is_small_double and path.p.count(r) < 2:
            yield r


def hashp(path):
    return "-".join(path)


def bfs_all(routes, next_state_x):
    begin_path = Path(["start"], False)
    q = deque([begin_path])
    seen = set()
    path_count = 0

    while len(q) > 0:
        path = q.popleft()
        path_hash = hashp(path.p)
        if path_hash in seen:
            continue
        seen.add(path_hash)

        for next_room in next_state_x(path, routes):
            next_p = path.p + [next_room]
            is_small_double = path.is_small_double
            if not is_small_double and not is_big(next_room) and next_room in path.p:
                is_small_double = True
            q.append(Path(next_p, is_small_double))

        if path.p[-1] == "end":
            path_count += 1

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
