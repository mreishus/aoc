#!/usr/bin/env python
"""
Advent Of Code 2024 Day 4
https://adventofcode.com/2024/day/4
"""
import re
from typing import List

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
    return rules, page_lists

def first_rule_broken( page_list, rules ):
    for i, page in enumerate(page_list):
        rules_say_before_this = []
        rules_say_after_this = []
        for left, right in rules:
            if left == page:
                rules_say_after_this.append(right)
            if right == page:
                rules_say_before_this.append(left)

        for j in range(len(page_list)):
            if j < i:
                # left
                target_page = page_list[j]
                if target_page in rules_say_after_this:
                    return j, i
            elif j == i:
                continue
            else:
                # right
                target_page = page_list[j]
                if target_page in rules_say_before_this:
                    return i, j
    return None, None

class Day05:
    """AoC 2024 Day 05"""

    @staticmethod
    def part1(filename: str) -> int:
        rules, page_lists = parse(filename)

        valid_total = 0
        for page_list in page_lists:
            is_valid = True
            for i, page in enumerate(page_list):
                rules_say_before_this = []
                rules_say_after_this = []
                for left, right in rules:
                    if left == page:
                        rules_say_after_this.append(right)
                    if right == page:
                        rules_say_before_this.append(left)

                rules_say_before_this = set(rules_say_before_this)
                rules_say_after_this = set(rules_say_after_this)

                before = set(page_list[:i])
                after = set(page_list[i+1:])

                violate1 = before & rules_say_after_this
                violate2 = after & rules_say_before_this

                if (len(violate1) > 0 or len(violate2) > 0):
                    is_valid = False
                    break
            if is_valid:
                middle_page = page_list[ len(page_list) // 2 ]
                valid_total += middle_page

        return valid_total

    @staticmethod
    def part2(filename: str) -> int:
        rules, page_lists = parse(filename)

        fixed_total = 0
        for page_list in page_lists:
            rules_broken = 0
            while True:
                i1, i2 = first_rule_broken( page_list, rules )
                if i1 is None or i2 is None:
                    break
                rules_broken += 1

                # use the information in X to swap
                page_list[i1], page_list[i2] = page_list[i2], page_list[i1]

            if rules_broken > 0:
                middle_page = page_list[ len(page_list) // 2 ]
                fixed_total += middle_page

        return fixed_total

