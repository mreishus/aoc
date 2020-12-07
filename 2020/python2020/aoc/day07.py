#!/usr/bin/env python
"""
Advent Of Code 2020 Day 7
https://adventofcode.com/2020/day/7
"""

import re
import functools
import sys

## A Bag has a pattern and a color
## Gotta learn an easier way to make a class
## that only holds two attributes (that's literally all it does)
class Bag:
    def __init__(self, pattern, color):
        self.pattern = pattern
        self.color = color

    def __repr__(self):
        return f"<Bag {self.pattern}, {self.color}>"

    def __eq__(self, another):
        return (
            hasattr(another, "pattern")
            and self.pattern == another.pattern
            and hasattr(another, "color")
            and self.color == another.color
        )

    def __hash__(self):
        return hash(self.pattern + self.color)


def parse(filename):
    with open(filename) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


# bright white bags contain 1 shiny gold bag.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# dotted black bags contain no other bags.
def parse_line(line):
    (pattern, color, rest) = re.match(r"(\w+) (\w+) bags contain (.*)$", line).groups()
    bag = Bag(pattern, color)
    inside = parse_rest(rest)
    return bag, inside


def parse_rest(line):
    if line == "no other bags.":
        return []

    clauses = line.split(", ")
    inside = []
    for clause in clauses:
        (qty, pattern, color) = re.match(r"(\d+) (\w+) (\w+) bag", clause).groups()
        bag = Bag(pattern, color)
        inside.append((int(qty), bag))
    return inside


def to_contain(data):
    contains = {}
    for (bag, inside) in data:
        if bag in contains:
            print("Duplicate definition, did not expect this")
            sys.exit()
        contains[bag] = inside
    return contains


def part1(contains):
    target = Bag("shiny", "gold")
    color_can_get_gold = {}

    @functools.cache
    def contains_gold(bag):
        return any(
            inner_bag == target or contains_gold(inner_bag)
            for (_qty, inner_bag) in contains[bag]
        )

    for bag in contains.keys():
        if bag.color in color_can_get_gold and color_can_get_gold[bag.color]:
            continue
        if contains_gold(bag):
            color_can_get_gold[bag] = True

    ## Incorrect guesses: 33 (I considered "dark red" and "spotted red" the same color
    ## The problem does not!)
    return len(color_can_get_gold.keys())


def part2(contains):
    need_to_check = set(contains.keys())
    have_checked = set()
    counts = {}

    def inside_count(bag):
        inside = contains[bag]
        if len(inside) == 0:
            return 0
        if bag in counts:
            return counts[bag]

        answer = sum(qty * (inside_count(a_bag) + 1) for (qty, a_bag) in inside)
        counts[bag] = answer
        return answer

    # Goes in right order, but possibly too much scanning
    while len(need_to_check) > 0:
        for this_bag in need_to_check.copy():
            inside = contains[this_bag]
            is_empty = len(inside) == 0
            is_figured_out = all(a_bag in have_checked for (qty, a_bag) in inside)
            if not (is_empty or is_figured_out):
                continue

            counts[this_bag] = inside_count(this_bag)

            have_checked.add(this_bag)
            need_to_check.remove(this_bag)

    return counts[Bag("shiny", "gold")]


class Day07:
    """ AoC 2020 Day 07 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 07 part 1 """
        data = parse(filename)
        contains = to_contain(data)
        return part1(contains)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 07 part 2 """
        data = parse(filename)
        contains = to_contain(data)
        return part2(contains)
