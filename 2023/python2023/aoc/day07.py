#!/usr/bin/env python
"""
Advent Of Code 2023 Day 7
https://adventofcode.com/2023/day/7
"""
import itertools


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    return line.split()


def rank_hand2_replace(hand):
    # Find the indexes of Js
    j_indexes = [i for i, x in enumerate(hand) if x == "J"]
    combos = []

    # Special cases
    num_j = len(j_indexes)
    if num_j == 0:
        return [hand]
    if num_j == 5:
        return ["AAAAA"]
    if num_j == 4:
        non_j = [x for x in hand if x != "J"][0]
        return [non_j * 5]

    # Replace Js
    replacements = itertools.product("23456789TQKA", repeat=num_j)
    for r in replacements:
        for i, j in enumerate(j_indexes):
            hand = hand[:j] + r[i] + hand[j + 1 :]
        combos.append(hand)
    return combos


def rank_hand2(hand):
    hands = rank_hand2_replace(hand)
    return min([rank_hand(x) for x in hands])


def rank_hand(hand):
    """Return the rank of a hand"""
    # 1. Five of a kind, where all five cards have the same label: AAAAA
    if len(set(hand)) == 1:
        return 1

    # 2. Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    if len(set(hand)) == 2:
        # 2. Four of a kind
        if hand.count(hand[0]) == 4 or hand.count(hand[1]) == 4:
            return 2

        # 3. Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        return 3

    # 4. Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    if len(set(hand)) == 3:
        # 4. Three of a kind
        if (
            hand.count(hand[0]) == 3
            or hand.count(hand[1]) == 3
            or hand.count(hand[2]) == 3
        ):
            return 4

        # 5. Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        return 5

    # 6. One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    if len(set(hand)) == 4:
        return 6

    # 7. High card, where all cards' labels are distinct: 23456
    return 7


def sort_key(hand):
    lookup = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
    }
    nhand = list(map(int, [lookup.get(x, x) for x in hand]))
    return (-1 * rank_hand(hand), nhand[0], nhand[1], nhand[2], nhand[3], nhand[4])


def sort_key2(hand):
    lookup = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "T": 10,
        "J": 1,
    }
    nhand = list(map(int, [lookup.get(x, x) for x in hand]))
    return (-1 * rank_hand2(hand), nhand[0], nhand[1], nhand[2], nhand[3], nhand[4])


class Day07:
    """AoC 2023 Day 07"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        data = sorted(data, key=lambda x: sort_key(x[0]))

        i = 1
        winnings = 0
        for hand, bid in data:
            score = int(bid) * i
            winnings += score
            i += 1
        return winnings

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        data = sorted(data, key=lambda x: sort_key2(x[0]))

        i = 1
        winnings = 0
        for hand, bid in data:
            # print(hand, bid, rank_hand2(hand))
            score = int(bid) * i
            winnings += score
            i += 1
        return winnings
