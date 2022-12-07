#!/usr/bin/env python
"""
Advent Of Code 2022 Day 07
https://adventofcode.com/2022/day/7
"""
import re

PARSER = re.compile(r"^\$ ([^\n]*)$(\n^[^$]*)?", re.MULTILINE)


def parse(filename):
    with open(filename) as file:
        parsed = []
        content = file.read().strip()
        matches = re.findall(PARSER, content)
        for (cmd, otpt) in matches:
            otpt = otpt.strip().splitlines()
            if len(otpt) == 0:
                otpt = None
            else:
                otpt = [line.split(" ") for line in otpt]
            parsed.append([cmd, otpt])
        return parsed


class Node:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.type = ""
        self.children = {}

    def find_path(self, patharray):
        if len(patharray) == 0:
            return self
        else:
            child = self.children[patharray[0]]
            return child.find_path(patharray[1:])

    def __repr__(self):
        return f"Node({self.name}, self.size={self.size}, self.type={self.type})"


def print_tree(a):
    print(a)
    for child in a.children.values():
        print_tree(child)


def build_fs(data):
    wd = []  # working directory
    fs = Node("")  # filesystem

    for [command, output] in data:
        if command.startswith("cd "):
            [_, path] = command.split(" ")
            if path == "/":
                wd = []
            elif path == "..":
                wd.pop()
            else:
                wd.append(path)
        elif command.startswith("ls"):
            node = fs.find_path(wd)
            for line in output:
                if line[0] == "dir":
                    newnode = Node(line[1])
                    newnode.type = "dir"
                    node.children[line[1]] = newnode
                else:
                    newnode = Node(line[1])
                    newnode.type = "file"
                    newnode.size = int(line[0])
                    node.children[line[1]] = newnode
    return fs


def get_size(a):
    if a.type == "file":
        return a.size
    return sum(get_size(b) for b in a.children.values())


def compute_all_sizes(a):
    a.size = get_size(a)
    for b in a.children.values():
        compute_all_sizes(b)


class Day07:
    """AoC 2022 Day 07"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        fs = build_fs(data)
        compute_all_sizes(fs)

        total_sizes_below_100k = 0

        def check(a):
            nonlocal total_sizes_below_100k
            if a.type == "dir" and a.size <= 100000:
                total_sizes_below_100k += a.size
            for child in a.children.values():
                check(child)

        check(fs)
        return total_sizes_below_100k

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        fs = build_fs(data)
        compute_all_sizes(fs)

        total_space = 70000000
        used_space = fs.size
        free_space = total_space - used_space
        target_free = 30000000

        deficit = target_free - free_space
        sizes_above_deficit = []

        def check(a):
            nonlocal sizes_above_deficit
            if a.type == "dir" and a.size > deficit:
                sizes_above_deficit.append(a.size)
            for child in a.children.values():
                check(child)

        check(fs)
        return min(sizes_above_deficit)
