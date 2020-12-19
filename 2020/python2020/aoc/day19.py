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
        # print(f"strings={strings}")
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
    rules, end_rules, strings = data
    # print("-begin-")
    # print(rules)
    # print("-loop-")

    a = 0
    while 0 not in end_rules:
        a += 1
        print(f"AAAAAAAA {a}")
        # print(end_rules)
        # print(rules)
        for k, v in rules.items():
            if k in end_rules:
                continue
            # print("--")
            # print(f"--{k}--")
            k_changed = False
            ki_changed_count = 0
            for i, possibility in enumerate(v):
                # print(i, possibility)
                if all(x in end_rules for x in possibility):
                    k_changed = True
                    ki_changed_count += 1
                    replacements = list(map(lambda n: rules[n], possibility))
                    # print(f"replacements {replacements}")
                    z = [reduce(operator.add, vals) for vals in product(*replacements)]
                    # print(f"======Z {len(z)}======= {z}")
                    rules[k][i] = z
            if k_changed:
                if all(list_all_string(l) for l in v):
                    end_rules.add(k)
                    # Flatten (1 level?)
                    rules[k] = list(chain(*rules[k]))

    ok_rules = set(rules[0])
    count = 0
    for s in strings:
        # print(s)
        if s in ok_rules:
            count += 1
    return count


def p2(data):
    rules, end_rules, strings = data
    print(rules[8])
    return -2


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
