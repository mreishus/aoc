#!/usr/bin/env python
"""
Advent Of Code 2024 Day 4
https://adventofcode.com/2024/day/4
"""
import re
from typing import List
from collections import defaultdict

def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

def parse(filename):
    with open(filename) as file:
        lines = file.read().strip()
        rules, page_lists = lines.split("\n\n")
        rules = rules.split("\n")
        rules = [ ints(rl) for rl in rules ]
        page_lists = page_lists.split("\n")
        page_lists = [ ints(l) for l in page_lists ]

    must_be_before_page = defaultdict(list)
    must_be_after_page  = defaultdict(list)
    for l, r in rules:
        must_be_before_page[r].append(l)
        must_be_after_page[l].append(r)

    return page_lists, must_be_before_page, must_be_after_page

def first_rule_broken( page_list, must_be_before_page, must_be_after_page ):
    for i, page in enumerate(page_list):
        must_befores = must_be_before_page[page]
        must_afters = must_be_after_page[page]

        for j in range(len(page_list)):
            if j < i:
                # left
                target_page = page_list[j]
                if target_page in must_afters:
                    return j, i
            elif j == i:
                continue
            else:
                # right
                target_page = page_list[j]
                if target_page in must_befores:
                    return i, j
    return None, None

class Day05:
    """AoC 2024 Day 05"""

    @staticmethod
    def part1(filename: str) -> int:
        page_lists, must_be_before_page, must_be_after_page = parse(filename)

        valid_total = 0
        for page_list in page_lists:
            is_valid = True
            for i, page in enumerate(page_list):
                must_befores = set(must_be_before_page[page])
                must_afters = set(must_be_after_page[page])

                before = set(page_list[:i])
                after = set(page_list[i+1:])

                if (len(before & must_afters) > 0 or len(after & must_befores) > 0):
                    is_valid = False
                    break
            if is_valid:
                middle_page = page_list[len(page_list) // 2]
                valid_total += middle_page

        return valid_total

    @staticmethod
    def part2(filename: str) -> int:
        page_lists, must_be_before_page, must_be_after_page = parse(filename)

        fixed_total = 0
        for page_list in page_lists:
            rules_broken = 0
            while True:
                i1, i2 = first_rule_broken(page_list, must_be_before_page, must_be_after_page)
                if i1 is None or i2 is None:
                    break
                rules_broken += 1

                # use the broken rule information to swap pages
                page_list[i1], page_list[i2] = page_list[i2], page_list[i1]

            if rules_broken > 0:
                middle_page = page_list[len(page_list) // 2]
                fixed_total += middle_page

        return fixed_total

