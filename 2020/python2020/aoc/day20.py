#!/usr/bin/env python
"""
Advent Of Code 2020 Day 20
https://adventofcode.com/2020/day/20
"""

from collections import defaultdict
from functools import reduce
from operator import mul
import re
import math
from typing import List, Dict, Tuple, Optional

from nptyping import NDArray
import numpy as np


class Tile:
    """Stores a tile as an 10x10 NPArray of 0 or 1, that can
    be rotated or flipped.  8 different orientations in total."""

    tile: NDArray
    tile_orig: NDArray
    orientation: int = (
        0  # How many 90 degree rotations. Add 4 if LR flipped. 0-7 possible values.
    )

    def __init__(self, tile: NDArray) -> None:
        self.tile = tile
        self.tile_orig = tile
        self.orientation = 0

    def __getitem__(self, item):
        """Allow direct access to self.tile when using [] on class instance."""
        return self.tile[item]

    def __setitem__(self, item, val):
        """Allow direct access to self.tile when using [] on class instance."""
        self.tile[item] = val

    def left(self) -> NDArray:
        """ Return left edge in the current orientation. """
        return self.tile[:, 0]

    def right(self) -> NDArray:
        """ Return right edge in the current orientation. """
        return self.tile[:, -1]

    def top(self) -> NDArray:
        """ Return top edge in the current orientation. """
        return self.tile[0, :]

    def bot(self) -> NDArray:
        """ Return bot edge in the current orientation. """
        return self.tile[-1, :]

    def set_orientation(self, new_o: int) -> None:
        """Given a orientation number 0-7, rearrange the tile to fit that orientation.
        0:   Original orientation.
        1-3: That many 90 degree turns.
        4:   Original orientation flipped L/R.
        5-7: Original orientation flipped L/R + 1-3 90 degree rotations.
        """
        self.orientation = new_o
        self.tile = self.tile_orig
        if new_o >= 4:
            self.tile = np.fliplr(self.tile)
            new_o -= 4
        self.tile = np.rot90(self.tile, new_o)

    def reorient(self) -> None:
        """ Reorient the tile by rotating and/or flipping. """
        self.set_orientation((self.orientation + 1) % 8)

    def destroy_edges(self) -> None:
        (y, x) = self.tile_orig.shape
        self.tile_orig = self.tile_orig[1 : y - 1, 1 : x - 1]

        (y, x) = self.tile.shape
        self.tile = self.tile[1 : y - 1, 1 : x - 1]


class Tiles:
    """ Stores a grouping of tiles.  """

    tiles: Dict[int, Tile]
    ids: List[int]
    edges4: Dict[
        int, List[NDArray]
    ]  # Given a tile ID, what 4 edges (original orientation) does it have?
    edges8: Dict[
        int, List[NDArray]
    ]  # Given a tile ID, what 8 edges (original + flipped) does it have?
    edge_lookup: Dict[
        bytes, List[int]
    ]  # Given an edge (1x10 array.tobytes()), which tile IDs does it belong to?
    grid: NDArray  # Grid of tileId locations in the completed puzzle
    orients: NDArray  # Grid of tile orientations in the completed puzzle
    puzzle: Optional[Tile]  # A tile containing the assembled puzzle, all pixels

    def __init__(self, tiles: Dict[int, Tile]):
        self.tiles = tiles  # dictionary of int -> np array
        self.ids = list(tiles.keys())
        self.clear_placements_grid()
        self.puzzle = None

        self.edges4 = {}
        self.edges8 = {}
        self.edge_lookup = defaultdict(list)
        self.compute_edges()

    def side_len(self):
        """If we arranged all tiles we have in one square, how long is a side?
        For the small example, it's 3. 3x3 = 9 tiles.
        For the real problem, it's 12. 12x12 = 144 tiles."""
        return int(math.sqrt(len(self.tiles)))

    def clear_placements_grid(self):
        side_len = self.side_len()
        self.grid = np.zeros([side_len, side_len], dtype=int)
        self.orients = np.zeros([side_len, side_len], dtype=int)

    def compute_edges(self):
        """ Fill the self.edges4, self.edges8, self.edge_lookup dictionaries. """
        for num, tile in self.tiles.items():
            edges4 = [tile.top(), tile.bot(), tile.left(), tile.right()]
            edges8 = edges4 + [np.flip(e) for e in edges4]
            self.edges4[num] = edges4
            self.edges8[num] = edges8
            for edge in edges8:
                self.edge_lookup[edge.tobytes()].append(num)

    def get_corners(self) -> List[int]:
        """ Find all tile ids which only have 2 edge matches to other tiles. """
        return [i for i in self.ids if self.edge_match_count(i) == 2]

    def edge_match_count(self, id1: int) -> int:
        """Given a tile id, find how many of its edges can find a match somewhere
        in the rest of the tiles. Returns 0-4. Corner pieces are 2, edge pieces are 3,
        middle pieces are 4, thanks to a puzzle design that allows these assumptions."""

        if len(self.edges4) != len(self.tiles) or id1 not in self.edges4:
            raise Exception("Invalid conditions")

        count = 0
        for edge in self.edges4[id1]:
            matches = self.edge_lookup[edge.tobytes()]
            matches = [m for m in matches if m != id1]
            count += len(matches)
        return count

    def top_matches(self, tile_id: int) -> List[int]:
        """ A list of tiles which can match tile_id's current top edge. """
        tile = self.tiles[tile_id]
        matches = self.edge_lookup[tile.top().tobytes()]
        return [m for m in matches if m != tile_id]

    def left_matches(self, tile_id: int) -> List[int]:
        """ A list of tiles which can match tile_id's current left edge. """
        tile = self.tiles[tile_id]
        matches = self.edge_lookup[tile.left().tobytes()]
        return [m for m in matches if m != tile_id]

    def right_matches(self, tile_id: int) -> List[int]:
        """ A list of tiles which can match tile_id's current right edge. """
        tile = self.tiles[tile_id]
        matches = self.edge_lookup[tile.right().tobytes()]
        return [m for m in matches if m != tile_id]

    def bot_matches(self, tile_id: int) -> List[int]:
        """ A list of tiles which can match tile_id's current bottom edge. """
        tile = self.tiles[tile_id]
        matches = self.edge_lookup[tile.bot().tobytes()]
        return [m for m in matches if m != tile_id]

    def find_match(self, edge: NDArray, tile_id: int) -> int:
        matches = self.edge_lookup[edge.tobytes()]
        matches = [m for m in matches if m != tile_id]
        if len(matches) != 1:
            raise Exception("Didn't find the right number of matches")
        return matches[0]

    def place_tiles(self):
        self.clear_placements_grid()
        side_len = self.side_len()

        ## Special Case: Fill top left corner
        top_left_id = self.get_corners()[0]
        top_left_tile = self.tiles[top_left_id]
        self.grid[0, 0] = top_left_id
        while (
            len(self.right_matches(top_left_id)) != 1
            or len(self.bot_matches(top_left_id)) != 1
        ):
            top_left_tile.reorient()

        self.orients[0, 0] = top_left_tile.orientation

        ## Special Case: Fill first row
        for x in range(1, side_len):
            left_id = self.grid[0, x - 1]
            right_edge = self.tiles[left_id].right()
            new_tile_id = self.find_match(right_edge, left_id)
            while not np.array_equal(
                self.tiles[left_id].right(), self.tiles[new_tile_id].left()
            ):
                self.tiles[new_tile_id].reorient()
            self.grid[0, x] = new_tile_id
            self.orients[0, x] = self.tiles[new_tile_id].orientation

        ## Now fill downward from each top row
        ## Only look for bottom edge + top edge matches, assume left-right works..
        for x in range(0, side_len):
            for y in range(1, side_len):
                top_id = self.grid[y - 1, x]
                bot_edge = self.tiles[top_id].bot()
                new_tile_id = self.find_match(bot_edge, top_id)
                while not np.array_equal(
                    self.tiles[top_id].bot(), self.tiles[new_tile_id].top()
                ):
                    self.tiles[new_tile_id].reorient()
                self.grid[y, x] = new_tile_id
                self.orients[y, x] = self.tiles[new_tile_id].orientation

        ## Double check the left-right matches that we ignored earlier, just
        ## for my peace of mind
        for y in range(0, side_len):
            for x in range(1, side_len):
                left_id = self.grid[y, x - 1]
                right_edge = self.tiles[left_id].right()

                right_id = self.grid[y, x]
                left_edge = self.tiles[right_id].left()

                if not np.array_equal(right_edge, left_edge):
                    raise Exception("Puzzle doesn't fit together")
        ## self.grid (matrix of tileIds) and self.orients (matrix of orientations)
        ## are now populated with the puzzle

    def stitch_puzzle(self):
        """Sets self.puzzle to a Tile containing the stitched together puzzle,
        after placing tiles and destroying their edges."""
        self.place_tiles()
        side_len = self.side_len()
        puzzle = np.zeros([8 * side_len, 8 * side_len], dtype=int)
        puzzle = Tile(puzzle)

        for y in range(side_len):
            for x in range(side_len):
                tile_id = self.grid[y, x]
                tile = self.tiles[tile_id]
                tile.set_orientation(self.orients[y, x])
                tile.destroy_edges()

                # print(tile.tile)
                # print(self.grid[y, x], self.orients[y, x], x, y)
                x_off = 8 * x
                y_off = 8 * y
                puzzle[0 + y_off : 8 + y_off, 0 + x_off : 8 + x_off] = (
                    self.grid[y, x] % 100
                )
                puzzle[0 + y_off : 8 + y_off, 0 + x_off : 8 + x_off] = tile.tile

        self.puzzle = puzzle

        # Reorient puzzle so it contains dragons
        dragon_count, water_roughness = self.find_dragons()
        for i in range(1, 8):
            if dragon_count > 0:
                break
            self.puzzle.set_orientation(i)
            dragon_count, water_roughness = self.find_dragons()

        return water_roughness

    def find_dragons(self):
        if self.puzzle is None:
            raise Exception("Find_Dragons: Need to stitch puzzle first")

        dragon = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3],
                [0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 0],
            ]
        )
        dragon_3_count = np.count_nonzero(dragon)
        (dragon_y_max, dragon_x_max) = dragon.shape
        (y_max, x_max) = self.puzzle.tile.shape

        dragon_count = 0
        for y in range(y_max - dragon_y_max + 1):
            for x in range(x_max - dragon_x_max + 1):
                # Look for dragon with top left corner at y, x
                sub_grid = self.puzzle[y : y + dragon_y_max, x : x + dragon_x_max]
                dragon_here = dragon_3_count == np.count_nonzero(dragon & sub_grid)

                if dragon_here:
                    ## Mark the dragon with "3"s in the puzzle
                    sub_grid |= dragon
                    dragon_count += 1

        water_roughness = np.count_nonzero(self.puzzle.tile == 1)
        return dragon_count, water_roughness


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
    return reduce(mul, t.get_corners())


def p2(data: Dict[int, Tile]) -> int:
    """ How many # are not part of a sea monster? """
    t = Tiles(data)
    water_roughness = t.stitch_puzzle()
    return water_roughness


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
