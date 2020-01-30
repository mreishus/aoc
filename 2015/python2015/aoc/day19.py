#!/usr/bin/env python
"""
Advent Of Code 2015 Day 19
https://adventofcode.com/2015/day/19
"""

from typing import Dict, List, Tuple, Set
from collections import defaultdict
from aoc.parsers import all_lines
from aoc.heapdict import heapdict


def parse(filename: str) -> Tuple[str, Dict[str, List[str]], Dict[str, List[str]]]:
    lines = all_lines(filename)

    begin = lines[-1]
    rules = defaultdict(list)
    rules_c = defaultdict(list)
    for line in lines[0:-2]:
        left, right = line.split(" => ")
        rules[left].append(right)
        rules_c[right].append(left)

    return begin, rules, rules_c


def part1(begin: str, rules: Dict[str, List[str]]) -> int:
    """ If we apply all of the rules once to STR, how many resulting strings are there? """
    return len(expand_rules(begin, rules))


def expand_rules(begin: str, rules: Dict[str, List[str]]) -> Set[str]:
    """ Apply the list of rules to a begin string, and return all new strings made. """
    strings_seen = set()
    for i, _ in enumerate(begin):
        for key_len in [1, 2]:
            to_replace = begin[i : i + key_len]
            before_char = begin[0:i]
            after_char = begin[i + key_len :]

            for replacement in rules[to_replace]:
                new_string = before_char + replacement + after_char
                strings_seen.add(new_string)
    return strings_seen


def contract(begin: str, rules: Dict[str, List[str]]) -> Set[str]:
    strings_seen = set()
    max_key_len = len(max(rules.keys(), key=len))

    key_lens_by_first_char = defaultdict(set)
    for key in rules.keys():
        key_lens_by_first_char[key[0]].add(len(key))

    begin_len = len(begin)
    for i, _ in enumerate(begin):
        if begin[i] not in key_lens_by_first_char:
            continue
        for key_len in key_lens_by_first_char[begin[i]]:
            # for key_len in range(1, max_key_len+1):
            if i + key_len > begin_len:
                continue
            to_replace = begin[i : i + key_len]
            if to_replace not in rules:
                continue

            before = begin[0:i]
            after = begin[i + key_len :]
            # print(f"{begin} | {i} {begin[i]} | {key_len} | {before} {to_replace} {after}")

            for replacement in rules[to_replace]:
                new_string = before + replacement + after
                strings_seen.add(new_string)

    return strings_seen


def heuristic(str1, str2) -> int:
    return abs(len(str1) - len(str2))


def part2(begin: str, rules: Dict[str, List[str]]) -> int:
    """ Use A star to find number of steps to contract string begin to "e". """
    goal = "e"
    closed_set = set()
    came_from = {}

    # Cost of travel -> this node
    travel_score = defaultdict(lambda: 999_999)
    travel_score[begin] = 0

    open_set = heapdict()
    open_set[begin] = heuristic(begin, goal)
    while len(open_set) > 0:
        (state, _) = open_set.popitem()
        if state == goal:
            return travel_score[state]

        closed_set.add(state)
        for new_state in contract(state, rules):
            if new_state in closed_set:
                continue
            cost = 1

            ## Unsure this is a correct/robust astar, since the problem doesn't demand it
            ## (Greedy algo works on this problem, so the astar doesn't have to be perfect to solve it)
            tenative_travel_score = travel_score[state] + cost
            if tenative_travel_score < travel_score[new_state]:
                came_from[new_state] = state
                travel_score[new_state] = tenative_travel_score
                if new_state not in open_set:
                    open_set[new_state] = tenative_travel_score + heuristic(new_state, goal)


class Day19:
    """ AoC 2015 Day 19 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 19 part 1 """
        begin, rules, rules_c = parse(filename)
        return part1(begin, rules)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 19 part 2 """
        target, rules, rules_c = parse(filename)
        return part2(target, rules_c)
