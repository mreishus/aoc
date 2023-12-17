#!/usr/bin/env python
"""
Advent Of Code 2023 Day 16
https://adventofcode.com/2023/day/16
"""
from collections import defaultdict


class Grid:
    def __init__(self):
        self.grid = {}
        self.is_lit = defaultdict(bool)
        self.max_x = 0
        self.max_y = 0

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    self.grid[(x, y)] = char
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def reset_lit(self):
        self.is_lit = defaultdict(bool)

    def part2(self):
        a = self.fire_all_right_edge_lasers()
        b = self.fire_all_left_edge_lasers()
        c = self.fire_all_top_edge_lasers()
        d = self.fire_all_bottom_edge_lasers()
        return max(a, b, c, d)

    def fire_all_left_edge_lasers(self):
        max_seen = 0
        for y in range(self.max_y):
            self.reset_lit()
            self.fire_laser(((0, y), "R"))
            lit = self.count_lit()
            max_seen = max(max_seen, lit)
        return max_seen

    def fire_all_right_edge_lasers(self):
        max_seen = 0
        for y in range(self.max_y):
            self.reset_lit()
            self.fire_laser(((self.max_x - 1, y), "L"))
            lit = self.count_lit()
            max_seen = max(max_seen, lit)
        return max_seen

    def fire_all_top_edge_lasers(self):
        max_seen = 0
        for x in range(self.max_x):
            self.reset_lit()
            self.fire_laser(((x, 0), "D"))
            lit = self.count_lit()
            max_seen = max(max_seen, lit)
        return max_seen

    def fire_all_bottom_edge_lasers(self):
        max_seen = 0
        for x in range(self.max_x):
            self.reset_lit()
            self.fire_laser(((x, self.max_y - 1), "U"))
            lit = self.count_lit()
            max_seen = max(max_seen, lit)
        return max_seen

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                print(self.grid[(x, y)], end="")
            print()

    def display_is_lit(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.is_lit[(x, y)]:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def fire_laser(self, laser=None):
        ## How should I define directions?
        if laser is None:
            laser = ((0, 0), "R")
        q = [laser]
        seen = set()
        while len(q) > 0:
            loc, direction = q.pop(0)

            x, y = loc
            ## out of bound check
            if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
                continue
            if (loc, direction) in seen:
                continue

            self.is_lit[loc] = True
            seen.add((loc, direction))

            if self.grid[loc] == ".":
                next_loc = self.next_loc(loc, direction)
                q.append((next_loc, direction))
            elif self.grid[loc] == "/" or self.grid[loc] == "\\":
                next_direction = self.next_direction(direction, self.grid[loc])
                next_loc = self.next_loc(loc, next_direction)
                q.append((next_loc, next_direction))
            elif self.grid[loc] == "|" or self.grid[loc] == "-":  ## Splitter
                is_pointy = None
                is_flat = None

                if self.grid[loc] == "|":
                    if direction == "U" or direction == "D":
                        is_pointy = True
                        is_flat = False
                    else:
                        is_pointy = False
                        is_flat = True
                elif self.grid[loc] == "-":
                    if direction == "L" or direction == "R":
                        is_pointy = True
                        is_flat = False
                    else:
                        is_pointy = False
                        is_flat = True

                if is_pointy:
                    ## In this case, just treat it like empty space.
                    next_loc = self.next_loc(loc, direction)
                    q.append((next_loc, direction))
                elif is_flat:
                    ## In this case, we need to split the beam.
                    next_direction1 = self.next_direction(direction, "/")
                    next_loc1 = self.next_loc(loc, next_direction1)
                    q.append((next_loc1, next_direction1))

                    next_direction2 = self.next_direction(direction, "\\")
                    next_loc2 = self.next_loc(loc, next_direction2)
                    q.append((next_loc2, next_direction2))
                else:
                    raise Exception(
                        "Impossible state: Mirror is neither pointy nor flat"
                    )
            else:
                raise Exception(f"Unknown character {self.grid[loc]}")

    def next_direction(self, direction, turn):
        if turn == "/":
            if direction == "R":
                return "U"
            elif direction == "L":
                return "D"
            elif direction == "U":
                return "R"
            elif direction == "D":
                return "L"
            else:
                raise Exception(f"Unknown direction {direction}")
        elif turn == "\\":
            if direction == "R":
                return "D"
            elif direction == "L":
                return "U"
            elif direction == "U":
                return "L"
            elif direction == "D":
                return "R"
            else:
                raise Exception(f"Unknown direction {direction}")
        else:
            raise Exception(f"Unknown turn {turn}")

    def next_loc(self, loc, direction):
        if direction == "R":
            return (loc[0] + 1, loc[1])
        elif direction == "L":
            return (loc[0] - 1, loc[1])
        elif direction == "U":
            return (loc[0], loc[1] - 1)
        elif direction == "D":
            return (loc[0], loc[1] + 1)
        else:
            raise Exception(f"Unknown direction {direction}")

    def count_lit(self):
        return sum(self.is_lit.values())


class Day16:
    """AoC 2023 Day 16"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        # print("")
        # g.display()
        g.fire_laser()
        # g.display_is_lit()
        return g.count_lit()

    @staticmethod
    def part2(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        return g.part2()
