#!/usr/bin/env python
"""
Advent Of Code 2020 Day 19
https://adventofcode.com/2020/day/19
"""

import re
from itertools import product, chain
from functools import reduce
import operator


def parse(filename):
    with open(filename) as f:
        lines = f.read().strip()
        rules, strings = lines.split("\n\n")
        strings = strings.strip().split("\n")
        rules, end_rules = parse_rules(rules)
        return rules, end_rules, strings


def parse_rules(rules_text):
    rules = {}
    end_rules = set()
    for line in rules_text.split("\n"):
        num, rest = line.split(": ")
        num = int(num)
        # print(f"{num}|||{rest}|||")
        if m := re.match(r"\"(\w+)\"", rest):
            char = m.groups()[0]
            rules[num] = [char]

            end_rules.add(int(num))
        else:
            z = []
            for clause in rest.split("|"):
                clause = clause.strip()
                clause_nums = list(map(int, clause.split(" ")))
                z.append(clause_nums)
            rules[num] = z

    return rules, end_rules


def list_all_string(l):
    return all(isinstance(item, str) for item in l)


def p1(data):
    rules, _end_rules, strings = p1_rules(data)

    ok_rules = set(rules[0])
    count = 0
    for s in strings:
        if s in ok_rules:
            count += 1
    return count


def p1_rules(data):
    rules, end_rules, strings = data

    while 0 not in end_rules:
        for k, v in rules.items():
            if k in end_rules:
                continue
            k_changed = False
            ki_changed_count = 0
            for i, possibility in enumerate(v):
                if all(x in end_rules for x in possibility):
                    k_changed = True
                    ki_changed_count += 1
                    replacements = list(map(lambda n: rules[n], possibility))
                    z = [reduce(operator.add, vals) for vals in product(*replacements)]
                    rules[k][i] = z
            if k_changed:
                if all(list_all_string(l) for l in v):
                    end_rules.add(k)
                    # Flatten (1 level?)
                    rules[k] = list(chain(*rules[k]))
    return rules, end_rules, strings


def p2(data):
    rules, end_rules, strings = data
    rules, end_rules, strings = p1_rules(data)

    # rules[8] = [[42], [42, 8]]
    # Or, rules[8] = (42)+

    # rules[11] = [[42, 31], [42, 11, 31]]
    # Or, Rules 11 = 42{X}31{X} if the Xs are the same amount

    # Rule 0 = Rule 8, then 11
    # Actually that means.. repeat 42 several times, then repeat 31 several times.
    # However, the number of 42s must be at least 1 more than the number of 31s.

    re_42 = "(" + "|".join(rules[42]) + ")"
    re_31 = "(" + "|".join(rules[31]) + ")"

    res = []
    for i in range(1, 10):
        for j in range(i + 1, 10):
            part_8 = "^(" + re_42 + "){" + str(j) + "}"
            part_11 = "(" + re_31 + "){" + str(i) + "}$"
            res.append(re.compile(part_8 + part_11))

    count = 0
    for s in strings:
        if any(this_re.match(s) for this_re in res):
            count += 1
    return count


class Day19:
    """ AoC 2020 Day 19 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 19 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 19 part 2 """
        data = parse(filename)
        return p2(data)
