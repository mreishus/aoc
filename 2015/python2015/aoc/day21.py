#!/usr/bin/env python
"""
Advent Of Code 2015 Day 21
https://adventofcode.com/2015/day/21
"""

from collections import namedtuple
from itertools import combinations, chain, product
from dataclasses import dataclass
import copy
from typing import List
from operator import attrgetter

Item = namedtuple("Item", ("name", "cost", "damage", "armor"))
ItemSet = namedtuple("ItemSet", ("names", "cost", "damage", "armor"))


@dataclass
class Char:
    hp: int
    damage: int
    armor: int


WEAPONS = [
    Item("Dagger", 8, 4, 0),
    Item("Shortsword", 10, 5, 0),
    Item("Warhammer", 25, 6, 0),
    Item("Longsword", 40, 7, 0),
    Item("Greataxe", 74, 8, 0),
]

ARMORS = [
    Item("None", 0, 0, 0),
    Item("Leather", 13, 0, 1),
    Item("Chainmail", 31, 0, 2),
    Item("Splintmail", 53, 0, 3),
    Item("Bandedmail", 75, 0, 4),
    Item("Platemail", 102, 0, 5),
]

RINGS = [
    Item("Dmg 1", 25, 1, 0),
    Item("Dmg 2", 50, 2, 0),
    Item("Dmg 3", 100, 3, 0),
    Item("Def 1", 20, 0, 1),
    Item("Def 2", 40, 0, 2),
    Item("Def 3", 80, 0, 3),
]


def collections() -> List[ItemSet]:
    rings = chain(
        combinations(RINGS, 2), combinations(RINGS, 1), combinations(RINGS, 0)
    )
    sets = []
    for (weapon, armor, rings) in product(WEAPONS, ARMORS, rings):
        # A little weirdness in flatting out the 0, 1, or 2 rings with 1 armor and 1 weapon
        items = rings + (weapon,) + (armor,)

        cost = sum(item.cost for item in items)
        names = ", ".join([item.name for item in items])
        damage = sum(item.damage for item in items)
        armor = sum(item.armor for item in items)

        itemset = ItemSet(names, cost, damage, armor)
        sets.append(itemset)
    return sets


def fight(char1, char2):
    """ Char1 and Char2 fight.  Returns True if Char1 wins. """
    char1 = copy.deepcopy(char1)
    char2 = copy.deepcopy(char2)
    while True:
        # Char1's turn
        dealt = max(1, char1.damage - char2.armor)
        char2.hp -= dealt
        if char2.hp <= 0:
            return True

        # Char2's turn
        dealt = max(1, char2.damage - char1.armor)
        char1.hp -= dealt
        if char1.hp <= 0:
            return False


def win(itemset, boss):
    player = Char(100, itemset.damage, itemset.armor)
    return fight(player, boss)


def part1(sets, boss):
    """ Given a list of item sets and a boss,
    gets the cost of the cheapest winning set. """
    winning_sets = [itemset for itemset in sets if win(itemset, boss)]
    cheapest_winning_set = min(winning_sets, key=attrgetter("cost"))
    # print("Cheapest winning set:")
    # print(cheapest_winning_set)
    return cheapest_winning_set.cost


def part2(sets, boss):
    """ Given a list of item sets and a boss,
    gets the cost of the most expensive losing set. """
    losing_sets = [itemset for itemset in sets if not win(itemset, boss)]
    expensive_losing_set = max(losing_sets, key=attrgetter("cost"))
    # print("Most expensive losing set:")
    # print(expensive_losing_set)
    return expensive_losing_set.cost


class Day21:
    """ AoC 2015 Day 21 """

    @staticmethod
    def part1(_filename: str) -> int:
        """ Given a filename, solve 2015 day 21 part 1 """
        sets = collections()
        boss = Char(104, 8, 1)  # Easier than parsing input.txt
        return part1(sets, boss)

    @staticmethod
    def part2(_filename: str) -> int:
        """ Given a filename, solve 2015 day 21 part 2 """
        sets = collections()
        boss = Char(104, 8, 1)  # Easier than parsing input.txt
        return part2(sets, boss)
