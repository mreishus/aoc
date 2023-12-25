#!/usr/bin/env python
"""
Advent Of Code 2023 Day 25
https://adventofcode.com/2023/day/25
"""
from collections import defaultdict
import random


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    left, right = line.split(": ")
    right_parts = right.split(" ")
    return left, right_parts


def get_reachable(connections, start):
    visited = set()
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            queue.extend(connections[node])
    return visited


def find_answer(connections):
    ## Find the two groups
    keys = list(connections.keys())
    group1 = get_reachable(connections, keys[0])
    size1 = len(group1)

    ## Find a key that's not in group 2
    key2 = None
    for key in keys:
        if key not in group1:
            key2 = key
            break

    group2 = get_reachable(connections, key2)
    size2 = len(group2)

    return size1 * size2


def get_shortest_path(connections, start, end):
    visited = set()
    queue = [(start, [start])]
    while queue:
        node, path = queue.pop(0)
        if node not in visited:
            visited.add(node)
            if node == end:
                return path
            for next_node in connections[node]:
                new_path = list(path)
                new_path.append(next_node)
                queue.append((next_node, new_path))


class Day25:
    """AoC 2023 Day 25"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        connections = defaultdict(list)
        flat_list = []
        flat_single_list = []
        for left, right_parts in data:
            for right in right_parts:
                connections[right].append(left)
                connections[left].append(right)
                flat_list.append((left, right))
                if left not in flat_single_list:
                    flat_single_list.append(left)

        start_node = flat_single_list[0]

        used_paths = defaultdict(int)
        for i in range(len(flat_single_list)):
            # print(i)
            # Getting paths between all nodes is too slow:
            # for j in range(i + 1, len(flat_single_list)):
            ## So take a random sample
            k = 5
            range_end = len(flat_single_list)
            sampled_elements = random.sample(
                range(i + 1, range_end), min(k, range_end - (i + 1))
            )
            for j in sampled_elements:
                if i == j:
                    continue
                path = get_shortest_path(
                    connections, flat_single_list[i], flat_single_list[j]
                )
                path_pairs = list(zip(path, path[1:]))
                for left, right in path_pairs:
                    left, right = sorted([left, right])
                    used_paths[(left, right)] += 1

        paths = []
        for item in used_paths.items():
            paths.append((item[1], item[0]))
        paths.sort(reverse=True)

        top_paths = paths[:10]
        # print(top_paths)
        for i in range(len(top_paths)):
            for j in range(i + 1, len(top_paths)):
                for k in range(j + 1, len(top_paths)):
                    _, (left1, right1) = top_paths[i]
                    _, (left2, right2) = top_paths[j]
                    _, (left3, right3) = top_paths[k]

                    connections[left1].remove(right1)
                    connections[right1].remove(left1)
                    connections[left2].remove(right2)
                    connections[right2].remove(left2)
                    connections[left3].remove(right3)
                    connections[right3].remove(left3)

                    reachable = get_reachable(connections, start_node)
                    # print("Looking for length:", len(flat_single_list))
                    # print("Found length:", len(reachable))
                    if len(reachable) != len(flat_single_list) and len(reachable) < len(
                        flat_single_list
                    ):
                        # print("Found answer, remove these pairs: ")
                        # print((left1, right1), (left2, right2), (left3, right3))
                        return find_answer(connections)

                    connections[left1].append(right1)
                    connections[right1].append(left1)
                    connections[left2].append(right2)
                    connections[right2].append(left2)
                    connections[left3].append(right3)
                    connections[right3].append(left3)
        return 0

    @staticmethod
    def part2(filename: str) -> int:
        return 0
