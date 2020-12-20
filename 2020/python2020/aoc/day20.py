#!/usr/bin/env python
"""
Advent Of Code 2020 Day 20
https://adventofcode.com/2020/day/20
"""

# from itertools import product, chain
# from functools import reduce
# import operator

import numpy as np
import re
import math

from typing import List, Set, Dict, Tuple, Optional, Any
from nptyping import NDArray


class Tile:
    """Stores a tile as an 10x10 NPArray of 0 or 1, that can
    be rotated or flipped.  8 different orientations in total."""

    tile: NDArray
    tile_orig: NDArray
    orientation: int = (
        0  # How many 90 degree rotations. Add 4 if LR flipped. 0-7 possible values.
    )

    def __init__(self, tile: NDArray):
        self.tile = tile
        self.tile_orig = tile
        self.orientation = 0

    def __getitem__(self, item):
        return self.tile[item]


class Tiles:
    """ Stores a grouping of tiles.  Not sure if this is staying around. """

    tiles: Dict[int, Tile]
    edges: Dict[int, List[NDArray]]

    def __init__(self, tiles: Dict[int, Tile]):
        self.tiles = tiles  # dictionary of int -> np array
        self.edges = {}

    def compute_edges(self):
        """ Fill the self.edges dictionary with a list of edges for each tile. """
        for num, tile in self.tiles.items():
            top = tile[0, :]
            bot = tile[-1, :]
            left = tile[:, 0]
            right = tile[:, -1]
            self.edges[num] = [top, bot, left, right]

    def edge_match_count(self, id1: int) -> int:
        """Given a tile id, find how many of its edges can find a match somewhere
        in the rest of the tiles. Returns 0-4. Corner pieces are 2, edge pieces are 3,
        middle pieces are 4, thanks to a puzzle design that allows these assumptions."""

        if len(self.edges) != len(self.tiles) or id1 not in self.edges:
            raise Exception("Invalid conditions")

        count = 0
        for edge in self.edges[id1]:
            edge_matched = False
            for k in self.edges.keys():
                if edge_matched or k == id1:
                    continue

                edges = self.edges[k]
                edges_f = [np.flip(e) for e in edges]
                if any(np.array_equal(e, edge) for e in edges + edges_f):
                    count += 1
                    edge_matched = True
        return count

    def place_tiles(self, corners):
        side_len = int(math.sqrt(len(self.tiles)))
        self.grid = np.zeros([side_len, side_len])  # Contains number indexs of tiles
        self.rot = np.zeros([side_len, side_len])  # Contains how many times was rotated
        self.flip = np.zeros([side_len, side_len])  # Contains if tile was flipped
        self.imag = np.zeros(
            [side_len, side_len]
        )  # Contains rotated image of each tile?
        self.grid[0, 0] = corners.pop()
        # self.rotate_top_left_corner()

    def is_match_right(self, id1, id2):
        """ Temp """
        if id1 not in self.tiles or id2 not in self.tiles:
            raise "tile not found"
        t1 = self.tiles[id1]
        t2 = self.tiles[id2]
        print(t1)
        print(self.tiles[1951])
        return False


def parse(filename: str) -> Dict[int, Tile]:
    """Read a filename into a dictionary mapping tile ids to Tile class
    instances."""
    with open(filename) as file:
        lines = file.read().strip()
        tiles_temp = [parse_tile(t) for t in lines.split("\n\n")]

        tiles = {}
        for (num, tile) in tiles_temp:
            tiles[num] = tile
        return tiles


def parse_tile(text: str) -> Tuple[int, Tile]:
    """Turn the text belonging to one tile into a tuple containing the tile id
    and the Tile class instance."""
    split_text = text.split("\n")
    num_text = split_text[0]
    tile_lines = split_text[1:]

    match = re.search(r"(\d+)", num_text)
    num = 0
    if match:
        num = int(match.groups()[0])
    else:
        raise Exception("Parse error")

    tile = np.array([parse_line(line.strip()) for line in tile_lines])
    return num, Tile(tile)


def parse_line(line: str) -> List[int]:
    """ Turn one line of a tile into a simple python array of 1s and 0s. """
    return [1 if char == "#" else 0 for char in line]


def p1(data: Dict[int, Tile]) -> int:
    """ What do you get if you multiply together the IDs of the four corner tiles? """
    t = Tiles(data)
    t.compute_edges()

    answer = 1
    for k in data.keys():
        if t.edge_match_count(k) == 2:
            answer *= k
    return answer


def p2(data: Dict[int, Tile]) -> int:
    """ How many # are not part of a sea monster? """
    t = Tiles(data)
    t.compute_edges()

    corners: List[int] = []
    for k in data.keys():
        if t.edge_match_count(k) == 2:
            corners.append(k)
    t.place_tiles(corners)
    return -2


class Day20:
    """ AoC 2020 Day 20 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 20 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 20 part 2 """
        data = parse(filename)
        return p2(data)
