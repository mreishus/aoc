#!/usr/bin/env python
"""
Advent Of Code 2020 Day 22
https://adventofcode.com/2020/day/22
"""

from collections import deque
from copy import deepcopy


def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip()
        p1, p2 = lines.split("\n\n")
        p1 = parse_player(p1)
        p2 = parse_player(p2)
        return p1, p2


def parse_player(lines):
    lines = lines.split("\n")
    return deque([int(x.strip()) for x in lines[1:]])


def p1(data):
    deck1, deck2 = data
    i = 1
    while len(deck1) > 0 and len(deck2) > 0:
        # print(f"Round {i}")
        # print(deck1, deck2)
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        # print(deck1, deck2)
        # print("")

        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        elif card1 < card2:
            deck2.append(card2)
            deck2.append(card1)
        else:
            raise Exception("No ties")
        i += 1

    if len(deck1) > 0:
        return score(deck1)
    elif len(deck2) > 0:
        return score(deck2)
    else:
        raise Exception("Both decks empty")


def score(deck):
    score = 0
    i = 1
    while len(deck) > 0:
        score += deck.pop() * i
        i += 1
    return score


def p2(data):
    deck1, deck2 = data
    deck1, deck2 = p2_game(deck1, deck2)
    if len(deck1) > 0:
        return score(deck1)
    elif len(deck2) > 0:
        return score(deck2)
    else:
        raise Exception("Both decks empty")


def p2_game(deck1, deck2):
    p2_seen = set()
    while len(deck1) > 0 and len(deck2) > 0:
        gamestate = (tuple(deck1), tuple(deck2))
        if gamestate in p2_seen:
            return deck1, deque()
        p2_seen.add(gamestate)

        card1 = deck1.popleft()
        card2 = deck2.popleft()

        if len(deck1) >= card1 and len(deck2) >= card2:
            # print("Subgame start")

            subdeck_1 = deepcopy(deck1)
            subdeck_2 = deepcopy(deck2)
            for _ in range(len(subdeck_1) - card1):
                subdeck_1.pop()
            for _ in range(len(subdeck_2) - card2):
                subdeck_2.pop()
            subdeck_1, subdeck_2 = p2_game(subdeck_1, subdeck_2)

            if len(subdeck_1) > 0:
                # print("P1 Won subgame")
                deck1.append(card1)
                deck1.append(card2)
            elif len(subdeck_2) > 0:
                # print("P2 won subgame")
                deck2.append(card2)
                deck2.append(card1)
            else:
                raise Exception("No ties")
        elif card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        elif card1 < card2:
            deck2.append(card2)
            deck2.append(card1)
        else:
            raise Exception("No ties")
    return deck1, deck2


class Day22:
    """ AoC 2020 Day 22 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 22 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 22 part 2 """
        data = parse(filename)
        return p2(data)
