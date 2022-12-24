#!/usr/bin/env python
"""
Advent Of Code 2022 Day 22
https://adventofcode.com/2022/day/22
"""
import re
from collections import defaultdict

PARSER = re.compile(r"(\d+)([L|R])?")
WARPS = 0


def parse(filename: str, small_input=False):
    """
    Parse the input file into a list of integers.
    Each integer is the sum of the numbers in a block.
    """
    with open(filename) as file:
        lines = file.read()
        maze, dirs = lines.split("\n\n")
        return parse_maze(maze, small_input), parse_dirs(dirs)


def parse_maze(maze, small_input=False):
    g = Grid()
    g.parse(maze, small_input)
    return g


def parse_dirs(dirs):
    r = []
    z = re.findall(PARSER, dirs)
    for (x, y) in z:
        r.append(int(x))
        if y:
            r.append(y)
    return r


class Grid:
    def __init__(self):
        self.grid = defaultdict(lambda: " ")
        self.max_x = 0
        self.max_y = 0
        self.init = None
        self.dir = (1, 0)
        #  RIGHT DOWN LEFT UP
        self.dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.regions = defaultdict(lambda: 0)

    def parse(self, data, small_input=False):
        for y, line in enumerate(data.splitlines()):
            for x, char in enumerate(line.rstrip("\n")):
                if char != " ":
                    self.grid[x, y] = char
                    if self.init is None and y == 0:
                        # print("Setting init to ", x, y)
                        self.init = (x, y)
                self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)

        if small_input:
            r1x = (8, 11)
            r1y = (0, 3)

            r2x = (0, 3)
            r2y = (4, 7)

            r3x = (4, 7)
            r3y = (4, 7)

            r4x = (8, 11)
            r4y = (4, 7)

            r5x = (8, 11)
            r5y = (8, 11)

            r6x = (12, 15)
            r6y = (8, 11)
        else:
            r1x = (50, 99)
            r1y = (0, 49)

            r2x = (100, 149)
            r2y = (0, 49)

            r3x = (50, 99)
            r3y = (50, 99)

            r4x = (50, 99)
            r4y = (100, 149)

            r5x = (0, 49)
            r5y = (100, 149)

            r6x = (0, 49)
            r6y = (150, 199)

        for x in range(r1x[0], r1x[1] + 1):
            for y in range(r1y[0], r1y[1] + 1):
                self.regions[x, y] = 1

        for x in range(r2x[0], r2x[1] + 1):
            for y in range(r2y[0], r2y[1] + 1):
                self.regions[x, y] = 2

        for x in range(r3x[0], r3x[1] + 1):
            for y in range(r3y[0], r3y[1] + 1):
                self.regions[x, y] = 3

        for x in range(r4x[0], r4x[1] + 1):
            for y in range(r4y[0], r4y[1] + 1):
                self.regions[x, y] = 4

        for x in range(r5x[0], r5x[1] + 1):
            for y in range(r5y[0], r5y[1] + 1):
                self.regions[x, y] = 5

        for x in range(r6x[0], r6x[1] + 1):
            for y in range(r6y[0], r6y[1] + 1):
                self.regions[x, y] = 6

        self.regions2 = [
            (None, None),
            (r1x, r1y),
            (r2x, r2y),
            (r3x, r3y),
            (r4x, r4y),
            (r5x, r5y),
            (r6x, r6y),
        ]

    def p1(self, instructions):
        loc = self.init
        for inst in instructions:
            if inst == "L":
                self.turn_left()
            elif inst == "R":
                self.turn_right()
            else:
                for _ in range(inst):
                    loc = self.move(loc)

        (x, y) = loc
        xx = x + 1
        yy = y + 1

        # print("Done:", xx, yy)
        # print("Facing: ", self.dir)
        # print("Facing index: ", self.dirs.index(self.dir))
        pw = 1000 * yy + 4 * xx + self.dirs.index(self.dir)
        # print("Final password: ", pw)
        return pw

    def next_tile(self, loc):
        x, y = loc
        dx, dy = self.dir
        x += dx
        y += dy
        if self.grid[x, y] == " ":
            # print("Trying to warp")
            ## Warp like pacman
            if self.dir == (1, 0):
                x = 0
                while self.grid[x, y] == " ":
                    x += 1
            elif self.dir == (-1, 0):
                x = self.max_x
                while self.grid[x, y] == " ":
                    x -= 1
            elif self.dir == (0, 1):
                y = 0
                while self.grid[x, y] == " ":
                    y += 1
            elif self.dir == (0, -1):
                y = self.max_y
                while self.grid[x, y] == " ":
                    y -= 1

        return x, y  # self.grid[x, y]

    def move(self, loc):
        x, y = loc
        xx, yy = self.next_tile(loc)
        if self.grid[xx, yy] == "#":
            # print("Hit a wall")
            return loc
        if self.grid[xx, yy] == " ":
            # print("Hit a warp- Should not happen")
            exit()
        return xx, yy

    def turn_right(self):
        i = self.dirs.index(self.dir)
        self.dir = self.get_dir(i + 1)

    def turn_left(self):
        i = self.dirs.index(self.dir)
        self.dir = self.get_dir(i - 1)

    def get_dir(self, i):
        return self.dirs[i % 4]

    def warp_map_small(self):
        """
                1111
                1111
                1111
                1111
        222233334444
        222233334444
        222233334444
        222233334444
                55556666
                55556666
                55556666
                55556666
        """
        #                0     1    2   3
        #  directions = right down left up
        return {
            (2, 1): (5, 3),  # Region 2 facing down: Warps to region 5 facing up
            (3, 3): (1, 0),  # Region 3 facing up: Warps to region 1 facing right
            (4, 0): (6, 1),  # Region 4 facing right: Warps to region 6 facing down
            (5, 1): (2, 3),  # Region 5 facing down: Warps to region 2 facing up
            (6, 1): (2, 0),  # Region 6 facing down: Warps to region 2 facing right
        }

    def warp_map(self, small_input=False):
        if small_input:
            return self.warp_map_small()
        """
        ...1#.2#
        ...##.##

        ...3#
        ...##

        5#.4#
        ##.##

        6#
        ##
        """
        #                0     1    2   3
        #  directions = right down left up
        return {
            (1, 2): (5, 0),  # Region 1 Facing left: Warps to Region 5 facing right
            (1, 3): (6, 0),  # Region 1 Facing up: Warps to Region 6 facing right
            (2, 0): (4, 2),  # Region 2 Facing right: Warps to Region 4 facing left
            (2, 1): (3, 2),  # Region 2 Facing down: Warps to Region 3 facing left
            (2, 3): (6, 3),  # Region 2 Facing up: Warps to Region 6 facing down
            (3, 0): (2, 3),  # Region 3 Facing right: Warps to Region 2 facing up
            (3, 2): (5, 1),  # Region 3 Facing left: Warps to Region 5 facing down
            (4, 0): (2, 2),  # Region 4 Facing right: Warps to Region 2 facing left
            (4, 1): (6, 2),  # Region 4 Facing down: Warps to Region 6 facing left
            (5, 2): (1, 0),  # Region 5 Facing left: Warps to Region 1 facing right
            (5, 3): (3, 0),  # Region 5 Facing up: Warps to Region 3 facing right
            (6, 0): (4, 3),  # Region 6 Facing right: Warps to Region 4 facing up
            (6, 1): (2, 1),  # Region 6 Facing down: Warps to Region 2 facing down
            (6, 2): (1, 1),  # Region 6 Facing left: Warps to Region 1 facing down
        }

    def p2(self, instructions, small_input=False):
        loc = self.init
        for inst in instructions:
            # print(" ==> ", inst)
            if inst == "L":
                self.turn_left()
            elif inst == "R":
                self.turn_right()
            else:
                for _ in range(inst):
                    loc = self.move2(loc, small_input=small_input)
                    # print(loc)

        (x, y) = loc
        xx = x + 1
        yy = y + 1

        # print("Done:", xx, yy)
        # print("Facing: ", self.dir)
        # print("Facing index: ", self.dirs.index(self.dir))
        pw = 1000 * yy + 4 * xx + self.dirs.index(self.dir)
        # print("Final password: ", pw)
        return pw

    def display(self):
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                print(self.regions[x, y], end="")
            print()

    def move2(self, loc, small_input=False):
        x, y = loc
        xx, yy, next_dir = self.next_tile2(loc, small_input=small_input)
        if self.grid[xx, yy] == "#":
            # print("Hit a wall", self.dir)
            return loc
        if self.grid[xx, yy] == " ":
            # print("Hit a warp- Should not happen")
            exit()
        self.dir = next_dir
        return xx, yy

    def dir_index_to_name(self, dir_index):
        if dir_index == 0:
            return "right"
        if dir_index == 1:
            return "down"
        if dir_index == 2:
            return "left"
        if dir_index == 3:
            return "up"

    def next_tile2(self, loc, small_input=False):
        global WARPS
        origx, origy = loc
        x, y = loc
        # print("Current loc: ", x, y)
        dx, dy = self.dir
        # print("Next tile: ", x, y)
        if self.grid[x + dx, y + dy] == " ":
            oldx, oldy = x, y
            current_region = self.regions[origx, origy]
            current_dir = self.dirs.index(self.dir)

            width = 50
            if small_input:
                width = 4

            offset = None
            #                0     1    2   3
            #  directions = right down left up
            if current_dir == 0:
                # offset = y % 50
                offset = y % width
            elif current_dir == 1:
                offset = x % width
            elif current_dir == 2:
                offset = y % width
            elif current_dir == 3:
                offset = x % width

            m = self.warp_map(small_input=small_input)
            if (current_region, current_dir) not in m:
                print(
                    f"Don't know how to warp from region={current_region} dir={current_dir}, WARPS={WARPS+1}"
                )
                exit()
            next_region, next_dir = m[current_region, current_dir]

            flip = False
            ## Warp from facing down to facing up, or any other opposite = Flip
            if (next_dir + 2) % 4 == current_dir:
                flip = True

            ## I might be missing some flip cases
            if current_dir == 0 and next_dir == 1:
                flip = True

            if flip:
                # offset = (49 - offset) % 50
                offset = ((width - 1) - offset) % width

            # print(
            #     f"Trying to warp from: region={current_region}, dir={current_dir}, offset={offset}, loc={x} {y}"
            # )
            # print(f"Warp to: region={next_region}, dir={next_dir}, offset={offset}")

            ((newx1, newx2), (newy1, newy2)) = self.regions2[next_region]
            # print("Target region X: ", newx1, newx2)
            # print("Target region Y: ", newy1, newy2)

            if next_dir == 0:  # Right
                x = newx1
                y = newy1 + offset
            elif next_dir == 1:  # down
                x = newx1 + offset
                y = newy1
            elif next_dir == 2:  # left
                x = newx2
                y = newy1 + offset
            elif next_dir == 3:  # up
                x = newx1 + offset
                y = newy2
            # print(
            #     f"Loc: ({oldx}, {oldy}) -> ({x}, {y}), dir=({self.dir_index_to_name(current_dir)} -> {self.dir_index_to_name(next_dir)})"
            # )
            # self.dir = self.get_dir(next_dir)
            WARPS += 1
            # if WARPS >= 13:
            #     print(f"Warps number {WARPS}, exiting")
            #     exit()
            return x, y, self.get_dir(next_dir)

        return x + dx, y + dy, self.dir  # self.grid[x, y]


class Day22:
    """AoC 2022 Day 22"""

    @staticmethod
    def part1(filename: str) -> int:
        maze, dirs = parse(filename)
        return maze.p1(dirs)

    @staticmethod
    def part2(filename: str) -> int:
        small_input = False
        if "input_small.txt" in filename:
            small_input = True
        maze, dirs = parse(filename, small_input=small_input)
        return maze.p2(dirs, small_input=small_input)


"""
SMALL
        1111    
        1111    
        1111    
        1111    
222233334444    
222233334444    
222233334444    
222233334444    
        55556666
        55556666
        55556666
        55556666

WARPMAP

Skipping this for now

1 = White top
2 = Blue back
3 = Orange Left
4 = Green front
5 = Yellow bottom
6 = Red right

LARGE

   1# 2#
   ## ##

   3#
   ##

5# 4#
## ##

6#
##

WARPMAP

1 UP    6 LEFT
1 LEFT  5 LEFT, FLIP
1 RIGHT 2 LEFT
1 DOWN  3 UP

2 UP    6 DOWN
2 LEFT  1 RIGHT
2 RIGHT 4 RIGHT, FLIP
2 DOWN  3 RIGHT

3 UP    1 DOWN
3 LEFT  5 UP
3 RIGHT 2 DOWN
3 DOWN  4 UP

4 UP    3 DOWN
4 LEFT  5 RIGHT
4 RIGHT 2 RIGHT, FLIP
4 DOWN  6 RIGHT

5 UP    3 LEFT
5 LEFT  1 LEFT, FLIP
5 RIGHT 4 LEFT
5 DOWN  6 UP

6 UP    5 DOWN
6 LEFT  1 UP
6 RIGHT 4 DOWN
6 DOWN  2 UP

1 = white top
2 = red right
3 = green front
4 = yellow bot
5 = orange left
6 = blue back
"""
