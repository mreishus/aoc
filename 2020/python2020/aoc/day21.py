#!/usr/bin/env python
"""
Advent Of Code 2020 Day 21
https://adventofcode.com/2020/day/21
"""

from collections import defaultdict
import re
from typing import Tuple, List


def parse(filename: str) -> List[Tuple[List[str], List[str]]]:
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line) -> Tuple[List[str], List[str]]:
    # mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    (items_str, contains_str) = re.match(r"^(.*)\(contains (.*)\)$", line).groups()
    items = items_str.strip().split(" ")
    contains = contains_str.strip().split(", ")
    return items, contains


def helpers(data):
    toxic_to_id = defaultdict(list)  # dairy => 0, 1
    toxic_to_candidates = {}  # fish => ['sqjhc', 'mxmxvkd'],
    all_items = set()
    known_safe = set()

    ## Build toxic_to_id
    for i, (items, contains) in enumerate(data):
        for toxic in contains:
            toxic_to_id[toxic].append(i)

    ## Build toxic_to_candidates
    for toxic, idxes in toxic_to_id.items():
        for i in idxes:
            if toxic not in toxic_to_candidates:
                toxic_to_candidates[toxic] = data[i][0]
            else:
                toxic_to_candidates[toxic] = [
                    d for d in data[i][0] if d in toxic_to_candidates[toxic]
                ]

    ## Build all_times
    for i, (items, contains) in enumerate(data):
        for item in items:
            all_items.add(item)

    ## Build known_safe
    for item in all_items:
        safe = True
        for candidates in toxic_to_candidates.values():
            if item in candidates:
                safe = False
                break
        if safe:
            known_safe.add(item)

    return toxic_to_id, toxic_to_candidates, all_items, known_safe


def p1(data):
    toxic_to_id, toxic_to_candidates, all_items, known_safe = helpers(data)

    ## How many times do safe items appear
    safe_count = 0
    for i, (items, contains) in enumerate(data):
        for item in items:
            if item in known_safe:
                safe_count += 1
    return safe_count
    # print(known_safe)

    # for i in idxes:
    #     print(data[i][0]
    #     candidates = data[i][0]
    return -1


def p2(data):
    toxic_to_id, toxic_to_candidates, all_items, known_safe = helpers(data)

    ### Figure out which is which
    ### Look at toxic to candidates:
    # {'dairy': ['mxmxvkd'], 'fish': ['sqjhc', 'mxmxvkd'], 'soy': ['sqjhc', 'fvjkl']}
    already_removed = set()
    while any(len(s) > 1 for s in toxic_to_candidates.values()):
        to_remove_val = None
        except_keep_key = None

        for k, v in toxic_to_candidates.items():
            if len(v) == 1 and v[0] not in already_removed:
                to_remove_val = v[0]
                except_keep_key = k
                break

        for k, v in toxic_to_candidates.items():
            if k == except_keep_key:
                continue
            toxic_to_candidates[k] = [item for item in v if item != to_remove_val]

        already_removed.add(to_remove_val)

    # t to c: {'dairy': 'mxmxvkd', 'fish': 'sqjhc', 'soy': 'fvjkl'}
    for k in toxic_to_candidates.keys():
        toxic_to_candidates[k] = toxic_to_candidates[k][0]

    # c to t: {'mxmxvkd': 'dairy', 'sqjhc': 'fish', 'fvjkl': 'soy'}
    candidate_to_toxic = dict(reversed(item) for item in toxic_to_candidates.items())

    sorted_toxins = sorted(toxic_to_candidates.keys())
    sorted_ingredients = list(map(lambda t: toxic_to_candidates[t], sorted_toxins))
    return ",".join(sorted_ingredients)


class Day21:
    """ AoC 2020 Day 21 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 21 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 21 part 2 """
        data = parse(filename)
        return p2(data)
