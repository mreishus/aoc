#!/usr/bin/env python
"""
Advent Of Code 2021 Day 12
https://adventofcode.com/2021/day/12
"""
from collections import defaultdict, Counter, deque


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


def next_states_p1(path, routes):
    loc = path[-1]
    if loc == "end":
        return []
    return [r for r in routes[loc] if is_big(r) or r not in path]


def next_states_p2(path, routes):
    loc = path[-1]
    if loc == "end":
        return []

    path_small = (r for r in path if not is_big(r))
    is_small_double = 2 in Counter(path_small).values()

    for r in routes[loc]:
        if r == "start":
            continue
        if is_big(r):
            yield r
        elif is_small_double and r not in path:
            yield r
        elif not is_small_double and path.count(r) < 2:
            yield r


def hashp(path):
    return "-".join(path)


def bfs_all(routes, next_state_x):
    q = deque([["start"]])
    seen = set()
    path_count = 0

    while len(q) > 0:
        path = q.popleft()
        path_hash = hashp(path)
        if path_hash in seen:
            continue
        seen.add(path_hash)

        for next_room in next_state_x(path, routes):
            q.append(path + [next_room])

        if path[-1] == "end":
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
