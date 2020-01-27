#!/usr/bin/env python
"""
Advent Of Code 2015 Day 13
https://adventofcode.com/2015/day/13
"""

import re
from typing import Dict, List, Set, Tuple, Union
from itertools import permutations
from aoc.parsers import all_lines

PARSER = re.compile(r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.")

def parse(lines: List[str]) -> Tuple[Set[str], Dict[Tuple[str, str], int]]:
    people = set()
    seating_pref = {}
    for line in lines:
        match = re.search(PARSER, line)
        if not match:
            raise ValueError("Can't parse this line")
        (subject, gainlose, amount, neighbor) = match.group(1, 2, 3, 4)

        amount = int(amount)
        if gainlose == "lose":
            amount *= -1

        people.add(subject)
        people.add(neighbor)
        seating_pref[(subject, neighbor)] = amount

    return people, seating_pref

def add_you(people: Set[str], seating_pref: Dict[Tuple[str, str], int]) -> Tuple[Set[str], Dict[Tuple[str, str], int]]:
    to_add = "You"
    for person in people:
        seating_pref[(person, to_add)] = 0
        seating_pref[(to_add, person)] = 0
    people.add(to_add)
    return people, seating_pref

def happiness_of_best(people: Set[str], seating_pref: Dict[Tuple[str, str], int]):
    perms = permutations(list(people))
    winner = max(perms, key=lambda people: happiness(people, seating_pref))
    return happiness(winner, seating_pref)

def happiness(people: Union[List[str], Tuple[str]], seating_pref: Dict[Tuple[str, str], int]):
    happiness = 0
    epeople = list(people) + [people[0]]
    for (p1, p2) in zip(epeople, epeople[1:]):
        happiness += seating_pref[(p1, p2)]
        happiness += seating_pref[(p2, p1)]
    return happiness


class Day13:
    """ AoC 2015 Day 13 """

    @staticmethod
    def part1(filename: str) -> str:
        """ Given a filename, solve 2015 day 13 part 1 """
        people, seating_pref = parse(all_lines(filename))
        return happiness_of_best(people, seating_pref)

    @staticmethod
    def part2(filename: str) -> str:
        """ Given a filename, solve 2015 day 13 part 2 """
        people, seating_pref = parse(all_lines(filename))
        people, seating_pref = add_you(people, seating_pref)
        return happiness_of_best(people, seating_pref)
