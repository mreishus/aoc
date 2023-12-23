#!/usr/bin/env python
"""
Advent Of Code 2023 Day 22
https://adventofcode.com/2023/day/22
"""
import re
from typing import List
from collections import defaultdict


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

    def load_pieces(self, filename):
        data = parse(filename)
        for (a, b, c), (x, y, z) in data:
            squares = []
            for i in range(a, x + 1):
                for j in range(b, y + 1):
                    for k in range(c, z + 1):
                        squares.append((i, j, k))

            self.add_piece(squares)

    def sort_pieces_by_z(self):
        self.pieces.sort(key=lambda piece: min(z for _, _, z in piece))

    def add_piece(self, piece):
        self.pieces.append(piece)

    def settle(self):
        did_something = True
        pieces_that_dropped = set()
        self.sort_pieces_by_z()
        while did_something:
            did_something = False
            self.build_lookup()
            for i in range(len(self.pieces)):
                if self.drop_piece(i):
                    pieces_that_dropped.add(i)
                    # print(f"dropped {i} --> {self.pieces[i]}")
                    did_something = True
        return len(pieces_that_dropped)

    def drop_piece(self, j):
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
        self.pieces.pop(i)
        v = self.settle()
        self.pieces = piece_copy

        return v


class Day22:
    """AoC 2023 Day 22"""

    @staticmethod
    def part1(filename: str) -> int:
        f = Field()
        f.load_pieces(filename)

        f.settle()
        f.build_support_tree()
        d_count = 0
        for i in range(len(f.pieces)):
            if f.can_be_disintegrated(i):
                d_count += 1
        return d_count

    @staticmethod
    def part2(filename: str) -> int:
        f = Field()
        f.load_pieces(filename)

        f.settle()
        f.build_support_tree()
        total = 0
        for i in range(len(f.pieces)):
            # print(f"Piece {i}: {f.pieces[i]} -- ", end="")
            if f.can_be_disintegrated(i):
                continue
            c_count = f.chain_reaction_count(i)
            total += c_count
            # print(f"chain reaction count: {c_count}")
        return total
