#!/usr/bin/env python

from collections import deque
from collections import defaultdict
# from aoc.computer import Computer, solve1
# from aoc.day21 import Day21
import re


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]

def parse_22(filename):
    data = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            # print(line)
            cut_match = re.match("^cut (-?\d+)", line)
            deal_inc_match = re.match("^deal with increment (\d+)", line)
            deal_new_match = re.match("^deal into new stack", line)
            if cut_match:
                [amount] = cut_match.groups()
                data.append(('cut', int(amount)))
            if deal_inc_match:
                [amount] = deal_inc_match.groups()
                data.append(('dealinc', int(amount)))
            if deal_new_match:
                data.append(('dealnew', None))
    return data

# (a, b) = re.match("person:(\w+) age:(\d+)", line).groups()

def part1(data, deck_size):
    deck = deque(range(deck_size))
    print(deck)
    for (command, arg) in data:
        # print("")
        # print(f"{command} {arg}")
        if command == "dealnew":
            deck = deque(reversed(deck))
            # print(deck)
        if command == "cut":
            # print("Before cut")
            # print(deck)
            deck.rotate(arg * -1)
            # print("After cut")
            # print(deck)
            # print(deck)
        if command == "dealinc":
            new_deck = [None] * len(deck)
            i = 0
            decklen = len(deck)
            # print("--")
            for j in range(decklen):
                item = deck.popleft()
                # print(f"Placing into spot {i}")
                new_deck[i] = item
                i = (i + arg) % decklen
            deck = deque(new_deck)
    return deck
    # print(deck)



if __name__ == "__main__":
    # data = parse_22("../../22/input_307.txt")
    # results = part1(data, 10)
    # print("3074185296:")
    # print(results)
    # print("")

    # data = parse_22("../../22/input_630.txt")
    # results = part1(data, 10)
    # print("6307418529:")
    # print(results)
    # print("")

    # data = parse_22("../../22/input_925.txt")
    # results = part1(data, 10)
    # print("9258147036:")
    # print(results)
    # print("")

    data = parse_22("../../22/input.txt")
    results = part1(data, 10_007)
    i = 0
    for i in results:
        if results[i] == 2019:
            print(i)
            break
        i += 1
    # 6835
    # (You guessed 9172.)
    # print(results[2019])

