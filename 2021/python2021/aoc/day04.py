#!/usr/bin/env python
"""
Advent Of Code 2021 Day 04
https://adventofcode.com/2021/day/4
"""
from typing import List
import re
from collections import defaultdict


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip()
        first, *blocks = lines.split("\n\n")
        return (first, blocks)


class Board:
    def __init__(self, lines):
        grid = defaultdict(int)  # coord -> Number on board
        marks = defaultdict(int)  # coord -> 0 or 1 if marked
        lookup = {}  # Number -> coord
        y = 0
        for line in lines.split("\n"):
            line = line.strip()
            x = 0
            for num in ints(line):
                grid[x, y] = num
                marks[x, y] = 0
                lookup[num] = (x, y)
                x += 1
            y += 1

        self.grid = grid
        self.marks = marks
        self.lookup = lookup

    def mark(self, number):
        if number not in self.lookup:
            return
        (x, y) = self.lookup[number]
        self.marks[x, y] = 1
        return self.is_winner()

    def unmarked_sum(self):
        s = 0
        for y in range(5):
            for x in range(5):
                if self.marks[x, y] == 0:
                    s += self.grid[x, y]
        return s

    def is_winner(self):
        for x in range(5):
            full_row = True
            for y in range(5):
                if self.marks[x, y] == 0:
                    full_row = False
                    break
            if full_row:
                return True

        for y in range(5):
            full_row = True
            for x in range(5):
                if self.marks[x, y] == 0:
                    full_row = False
                    break
            if full_row:
                return True

        return False


class Day04:
    """ AoC 2021 Day 04 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 04 part 1 """
        (first, boards_raw) = parse(filename)

        boards = []
        for board_raw in boards_raw:
            boards.append(Board(board_raw))

        nums = ints(first)
        for num in nums:
            for board in boards:
                winner = board.mark(num)
                if winner:
                    return num * board.unmarked_sum()
        return None

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 04 part 2 """
        (first, boards_raw) = parse(filename)

        boards = []
        for board_raw in boards_raw:
            boards.append(Board(board_raw))

        nums = ints(first)
        winner_boards = {}
        for num in nums:
            for i, board in enumerate(boards):
                if i in winner_boards:
                    continue
                winner = board.mark(num)
                if winner:
                    if (len(winner_boards) + 1) == len(boards):
                        return num * board.unmarked_sum()
                    winner_boards[i] = True
        return None
