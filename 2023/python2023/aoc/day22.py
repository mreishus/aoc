#!/usr/bin/env python
"""
Advent Of Code 2023 Day 22
https://adventofcode.com/2023/day/22
"""
import re
from typing import List
from collections import defaultdict
from functools import cache


def parse(filename: str):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    a, b, c, x, y, z = ints(line)
    return (a, b, c), (x, y, z)


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


class Field:
    def __init__(self):
        self.pieces = []
        self.lookup = {}
        self.is_supported_by = defaultdict(list)
        self.supports = defaultdict(list)

    def add_piece(self, piece):
        self.pieces.append(piece)

    def settle(self):
        did_something = True
        pieces_that_dropped = set()
        while did_something:
            did_something = False
            self.build_lookup()
            # print("built lookup")
            for i in range(len(self.pieces)):
                # if self.drop_piece(i):
                if self.drop_piece_new(i):
                    pieces_that_dropped.add(i)
                    # print(f"dropped {i} --> {self.pieces[i]}")
                    did_something = True
                    break
        return len(pieces_that_dropped)

    def drop_piece(self, j):
        squares = self.pieces[j]

        below_squares = []
        for square in squares:
            if square[2] <= 1:
                return False
            below_squares.append((square[0], square[1], square[2] - 1))

        can_drop = True
        for i in range(len(self.pieces)):
            if not can_drop:
                break
            if i == j:
                continue

            for that_square in self.pieces[i]:
                if not can_drop:
                    break

                for this_square in below_squares:
                    if this_square == that_square:
                        can_drop = False
                        break

        if can_drop:
            print(f"dropping {j}")
            self.pieces[j] = below_squares
            return True
        return False

    def drop_piece_new(self, j):
        ## We assume lookup has been built.
        squares = self.pieces[j]

        possible_drop_amounts = []
        for s in squares:
            ## Look down until we find either a square or the ground.
            drop_amount = 0
            while True:
                below_square = (s[0], s[1], (s[2] - drop_amount) - 1)
                hit_ground = below_square[2] == 0
                is_blocked = (
                    below_square in self.lookup and self.lookup[below_square] != j
                )
                if hit_ground or is_blocked:
                    break
                drop_amount += 1

            possible_drop_amounts.append(drop_amount)
            if drop_amount == 0:
                break

        if len(possible_drop_amounts) == 0:
            return False

        drop_amount = min(possible_drop_amounts)
        if drop_amount == 0:
            return False

        new_squares = []
        for s in squares:
            new_squares.append((s[0], s[1], s[2] - drop_amount))
        self.pieces[j] = new_squares
        return True

    def build_lookup(self):
        lookup = {}
        for i in range(len(self.pieces)):
            for square in self.pieces[i]:
                lookup[square] = i
        self.lookup = lookup

    def build_support_tree(self):
        self.build_lookup()
        is_supported_by = defaultdict(list)
        supports = defaultdict(list)

        for i in range(len(self.pieces)):
            for square in self.pieces[i]:
                above_square = (square[0], square[1], square[2] + 1)
                if above_square in self.lookup:
                    above_piece = self.lookup[above_square]
                    if above_piece == i:
                        continue

                    ## Above_piece supports i
                    supports[i].append(above_piece)
                    is_supported_by[above_piece].append(i)

        self.is_supported_by = is_supported_by
        self.supports = supports

    def can_be_disintegrated(self, i):
        ## Which do I support?
        if len(self.supports[i]) == 0:
            return True

        ## Otherwise, check the ones that I support. If they all have some other
        ## block supporting them, then it's ok to be disintegrated.
        for j in self.supports[i]:
            consider = self.is_supported_by[j]

            consider_temp = [x for x in consider if x != i]
            if len(consider_temp) == 0:
                return False
        return True

    def chain_reaction_count(self, i):
        piece_copy = self.pieces.copy()
        self.pieces[i] = []
        print(f"chain reaction count for {i}")
        v = self.settle()
        self.pieces = piece_copy

        return v


class Day22:
    """AoC 2023 Day 22"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)

        f = Field()

        for (a, b, c), (x, y, z) in data:
            squares = []
            for i in range(a, x + 1):
                for j in range(b, y + 1):
                    for k in range(c, z + 1):
                        squares.append((i, j, k))

            f.add_piece(squares)

        print("start to settle")
        f.settle()
        print("start to build tree")
        f.build_support_tree()
        print("--")
        # print("Is supported by")
        # print(f.is_supported_by)
        # print("Supports")
        # print(f.supports)
        d_count = 0
        for i in range(len(f.pieces)):
            # print(f"Piece {i}: {f.pieces[i]} -- ", end="")
            if f.can_be_disintegrated(i):
                d_count += 1
                # print("CAN be disintegrated")
            # else:
            #     print("cannot be disintegrated")
        return d_count

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)

        f = Field()

        for (a, b, c), (x, y, z) in data:
            squares = []
            for i in range(a, x + 1):
                for j in range(b, y + 1):
                    for k in range(c, z + 1):
                        squares.append((i, j, k))

            f.add_piece(squares)

        print("start to settle")
        f.settle()
        print("start to build tree")
        f.build_support_tree()
        print("--")
        # print("Is supported by")
        # print(f.is_supported_by)
        # print("Supports")
        # print(f.supports)
        total = 0
        for i in range(len(f.pieces)):
            print(f"Piece {i}: {f.pieces[i]} -- ", end="")
            c_count = f.chain_reaction_count(i)
            total += c_count
            print(f"chain reaction count: {c_count}")
            # else:
            #     print("cannot be disintegrated")
        return total
        ## Wrong: 20569
