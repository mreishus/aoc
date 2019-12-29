#!/usr/bin/env python
from aoc.day10 import knot_hash


def hexify(string):
    return bin(int(string, 16))[2:]


def part1(magic):
    return magic_to_count(magic)


def part2(magic):
    grid = magic_to_grid(magic)
    rf = RegionFinder(grid)
    count = rf.find_regions()
    return count


class RegionFinder:
    def __init__(self, grid):
        self.grid = grid

    def gen_neighbors(self, coord):
        """ Given a tuple coordinate, return a generator iterating over
        its 4 direct neighbors """
        (x, y) = coord
        yield (x + 1, y)
        yield (x - 1, y)
        yield (x, y + 1)
        yield (x, y - 1)

    def find_regions(self):
        count = 1
        # Not that robust: Assuming grid has (x, y) keys with range 0-127
        for y in range(128):
            for x in range(128):
                val = self.grid[(x, y)]
                if val == "x":
                    self.dfs((x, y), count)
                    count += 1
        return count - 1

    def dfs(self, coord, region_num):
        self.grid[coord] = region_num
        for n_coord in self.gen_neighbors(coord):
            if n_coord not in self.grid:
                continue
            if self.grid[n_coord] == "x":
                self.dfs(n_coord, region_num)


def magic_to_grid(magic):
    """ Converts a magic number to a 128x128 grid as
    defined by the problem.
    The grid is represented as a map with (x, y) keys.
    Values are either 0 if blank, or "x" if filled in, but unassigned
    to a region.  Values are this weird mix of types so we can use
    1-99+ as region identifiers. """
    grid = {}
    for y in range(128):
        key = magic + "-" + str(y)
        list_of_strings_hash = [
            hexify(letter).zfill(4) for letter in list(knot_hash(key))
        ]
        x = 0
        for string in list_of_strings_hash:
            for char in string:
                location = (x, y)
                grid[location] = 0 if char == "0" else "x"
                x += 1
    return grid


def magic_to_count(magic):
    count = 0
    for i in range(128):
        key = magic + "-" + str(i)
        list_of_strings_hash = [
            hexify(letter).zfill(4) for letter in list(knot_hash(key))
        ]
        for string in list_of_strings_hash:
            count += sum(1 for letter in list(string) if letter == "1")
    return count


if __name__ == "__main__":
    magic = "flqrgnkx"  # Example
    magic = "hfdlxzhv"  # Mine
    print("Part1: ")
    print(part1(magic))
    print("Part2: ")
    print(part2(magic))
