#!/usr/bin/env python
from collections import defaultdict
import string


class Grid:
    def __init__(self, filename):
        self.grid = defaultdict(lambda: " ")
        self.load_file(filename)

    def load_file(self, filename):
        grid = defaultdict(lambda: " ")
        with open(filename) as f:
            y = 0
            for line in f.readlines():
                line = line.strip("\n")
                x = 0
                for char in line:
                    grid[complex(x, y)] = char
                    x += 1
                y += 1
        self.grid = grid

    def range(self):
        reals = [c.real for c in self.grid.keys()]
        imags = [c.imag for c in self.grid.keys()]
        return {
            "min_x": int(min(reals)),
            "max_x": int(max(reals)),
            "min_y": int(min(imags)),
            "max_y": int(max(imags)),
        }


def turn_right(direction):
    return direction * complex(0, 1)


def turn_left(direction):
    return direction * complex(0, -1)


class Day19:
    def __init__(self, filename):
        self.g = Grid(filename)

    def start_coord(self):
        y = 0
        for x in range(9999):
            if self.g.grid[complex(x, y)] == "|":
                return complex(x, y)
        raise ValueError("Couldn't find first coordinate")

    def part1_and_2(self):
        # Start here
        location = self.start_coord()
        direction = complex(0, 1)
        steps = 0
        letters_seen = []

        while True:
            this_square = self.g.grid[location]
            if this_square in string.ascii_uppercase:
                letters_seen.append(this_square)

            next_square = self.g.grid[location + direction]
            if next_square == " ":
                right_square = self.g.grid[location + turn_right(direction)]
                left_square = self.g.grid[location + turn_left(direction)]
                if right_square != " ":
                    direction = turn_right(direction)
                elif left_square != " ":
                    direction = turn_left(direction)
                else:
                    break

            location += direction
            steps += 1

        p1_ans = "".join(letters_seen)
        p2_ans = steps + 1
        return p1_ans, p2_ans


if __name__ == "__main__":
    d19 = Day19("../input_small.txt")
    print(d19.part1_and_2())
    d19 = Day19("../input.txt")
    print(d19.part1_and_2())
