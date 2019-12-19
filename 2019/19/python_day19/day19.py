#!/usr/bin/env python

from os import system
from collections import defaultdict
from aoc.computer import Computer, solve1


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


def manhattan(coord):
    return abs(coord.real) + abs(coord.imag)


class Day19:
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])
        self.grid = defaultdict(lambda: "?")
        self.filled_squares = {}

    def part1(self):
        print("Part1")
        count = 0
        for x in range(50):
            for y in range(50):
                this_value = solve1(self.program, [x, y])[0]
                # print(f"Got value {this_value}")
                if this_value == 1:
                    count += 1

        print("part1:")
        print(count)

    def part2(self):
        print("Constructing")

        x_started = None
        x_ended = None
        for y in range(1700):
            use_opt = y > 6
            scan_range = range(10)

            if use_opt and x_started is not None:
                scan_range = range(x_started, 50)
            if use_opt and x_started is not None and x_stopped is not None:
                scan_range = range(x_started, x_stopped + 3)

            seen_light = False
            x_stopped = None
            for x in scan_range:
                this_value = solve1(self.program, [x, y])[0]
                self.grid[complex(x, y)] = this_value
                if this_value == 1:
                    self.filled_squares[complex(x, y)] = 1
                    if seen_light == False:
                        seen_light = True
                        x_started = x
                if this_value == 0 and seen_light == True and x_stopped is None:
                    x_stopped = x
        print("Done Constructing")

        # self.display()

        squares = sorted(self.filled_squares.keys(), key=manhattan)
        size = 99

        print("Looking")
        for square in squares:
            if (
                square in self.filled_squares
                and square + complex(size, 0) in self.filled_squares
                and square + complex(0, size) in self.filled_squares
                and square + complex(size, size) in self.filled_squares
            ):
                print("------")
                print(square)
                print(int(square.real) * 10_000 + int(square.imag))

                #                 self.grid[square] = "O"
                #                 self.grid[square + complex(0, size)] = "O"
                #                 self.grid[square + complex(size, size)] = "O"
                #                 self.grid[square + complex(size, 0)] = "O"
                #                 self.display()
                break

    def display(self):
        reals = [c.real for c in self.grid.keys() if self.grid[c] != 9]
        imags = [c.imag for c in self.grid.keys() if self.grid[c] != 9]
        for y in range(int(min(imags)) - 0, int(max(imags)) + 0):
            for x in range(int(min(reals)) - 0, int(max(reals)) + 0):
                char = self.grid[complex(x, y)]
                print(char, end="")
            print("")


# Wrong guess: 15791361 (Size = 100)
# Correct answer (size = 99) ??
if __name__ == "__main__":
    program = parse("../../19/input.txt")
    d9 = Day19(program)
    d9.part1()
    d9.part2()
