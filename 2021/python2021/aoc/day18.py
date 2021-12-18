#!/usr/bin/env python
"""
Advent Of Code 2021 Day 18
https://adventofcode.com/2021/day/18
"""
from typing import List
import re
from math import floor, ceil


def parse(filename: str):
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "[" + repr(self.left) + "," + repr(self.right) + "]"

    def __eq__(self, other):
        return (
            isinstance(other, Pair)
            and self.left == other.left
            and self.right == other.right
        )


def build_tree(line):
    a = 0
    b = len(line) - 1

    def parse(a, b):
        if line[a] == "[" and line[b] == "]":
            level = 0
            left_start = a + 1
            left_end = None
            right_start = None
            right_end = b - 1
            for i in range(a + 1, b - 1 + 1):
                if line[i] == "[":
                    level += 1
                elif line[i] == "]":
                    level -= 1
                elif line[i] == "," and level == 0:
                    left_end = i - 1
                    right_start = i + 1
            return Pair(parse(left_start, left_end), parse(right_start, right_end))
        elif a == b and line[a].isdigit():
            return int(line[a])

    return parse(a, b)


def leftmost(root):
    if root is None or isinstance(root, int):
        return root
    return leftmost(root.left)


def rightmost(root):
    if root is None or isinstance(root, int):
        return root
    return rightmost(root.right)


def explode(root):
    exploded = False

    def check(pair, level, leftNode=None, rightNode=None):
        nonlocal exploded
        if exploded or isinstance(pair, int):
            return pair
        if level > 4:
            exploded = True
            if rightNode is not None:
                if isinstance(rightNode.right, Pair):
                    target = rightNode.right
                    while isinstance(target.left, Pair):
                        target = target.left
                    target.left += pair.right
                else:
                    rightNode.right += pair.right
            if leftNode is not None:
                if isinstance(leftNode.left, Pair):
                    target = leftNode.left
                    while isinstance(target.right, Pair):
                        target = target.right
                    target.right += pair.left
                else:
                    leftNode.left += pair.left
            return 0

        pair.left = check(pair.left, level + 1, leftNode, pair)
        pair.right = check(pair.right, level + 1, pair, rightNode)
        return pair

    return check(root, 1), exploded


def do_split(num):
    left = floor(num / 2)
    right = ceil(num / 2)
    return Pair(left, right)


def rsplit(root):
    did_split = False

    def check(pair):
        nonlocal did_split
        if did_split:
            return pair
        if isinstance(pair, int):
            if pair >= 10:
                did_split = True
                return do_split(pair)
            return pair

        pair.left = check(pair.left)
        pair.right = check(pair.right)
        return pair

    return check(root), did_split


def reduce(root):
    while True:
        root, exploded = explode(root)
        if exploded:
            continue
        root, did_split = rsplit(root)
        if did_split:
            continue
        break
    return root


def add(root1, root2):
    return Pair(root1, root2)


def magnitude(root):
    if isinstance(root, int):
        return root
    return 3 * magnitude(root.left) + 2 * magnitude(root.right)


class Day18:
    """ AoC 2021 Day 18 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 18 part 1 """
        data = parse(filename)
        root = build_tree(data[0])
        for line in data[1:]:
            root = reduce(add(root, build_tree(line)))
        return magnitude(root)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 18 part 2 """
        data = parse(filename)

        def add_mag(i, j):
            root1 = build_tree(data[i])
            root2 = build_tree(data[j])
            return magnitude(reduce(add(root1, root2)))

        m_max = 0
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                for m in [add_mag(i, j), add_mag(j, i)]:
                    m_max = max(m_max, m)

        return m_max
