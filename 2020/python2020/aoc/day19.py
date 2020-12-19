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
    rules, end_rules, strings = p1_rules(data)

    ok_rules = set(rules[0])
    count = 0
    for s in strings:
        # print(s)
        if s in ok_rules:
            count += 1
    return count


def p1_rules(data):
    rules, end_rules, strings = data
    # print("-begin-")
    # print(rules)
    # print("-loop-")

    a = 0
    while 0 not in end_rules:
        a += 1
        print(f"AAAAAAAA {a}")
        # print(end_rules)
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
    return rules, end_rules, strings


def p2(data):
    rules, end_rules, strings = data
    rules, end_rules, strings = p1_rules(data)

    # rules[8] = [[42], [42, 8]]
    # Or, rules[8] = (42)+

    # rules[11] = [[42, 31], [42, 11, 31]]
    # Or, Rules 11 = 42{X}31{X} if the Xs are the same amount

    # Rule 0 = Rule 8, then 11
    # Actually that means.. repeat 42 as many times as you want,
    # then repeat 31 0 to infinity times?

    re_42part = "(" + "|".join(rules[42]) + ")+"
    re_31part = "(" + "|".join(rules[31]) + ")+$"

    my_re_s = re_42part + re_31part
    # print(my_re_s)
    my_re = re.compile(my_re_s)

    # 445 too high
    # 439 too high, unlucky
    count = 0
    for s in strings:
        if my_re.match(s):
            # print(s)
            count += 1
    return count

    # print("42")
    # print(rules[42])
    # print("31")
    # print(rules[31])

    # Matt:
    # These are too hard, let's manually
    # expand them up to 3 times?

    # rules[8] = []
    # for i in range(1, 2):
    #     rules[8].append([42] * i)

    # rules[11] = []
    # for i in range(1, 2):
    #     rules[11].append([42] * i + [31] * i)
    # print(rules[11])

    # return p1((rules, end_rules, strings))


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
