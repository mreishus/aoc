#!/usr/bin/env python

from collections import defaultdict
from aoc.computer import Computer
from aoc.day15 import Day15
from os import system


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


class RepairDroid:
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])
        self.grid = defaultdict(lambda: 0)

    def load_pic(self):
        result = self.execute()
        location = complex(0, 0)
        for num in result:
            if num == 10:
                new_imag = int(location.imag + 1)
                location = complex(0, new_imag)
            else:
                char = chr(num)
                self.grid[location] = char
                location += complex(1, 0)

    def execute(self):
        self.cpu.execute()
        result = []
        while self.cpu.has_output():
            result.append(self.cpu.pop_output())
        return result

    def display(self):
        reals = [c.real for c in self.grid.keys() if self.grid[c] != 0]
        imags = [c.imag for c in self.grid.keys() if self.grid[c] != 0]
        system("clear")
        for y in range(int(min(imags)) - 2, int(max(imags)) + 3):
            for x in range(int(min(reals)) - 2, int(max(reals)) + 3):
                char = self.grid[complex(x, y)]
                print(char, end="")
            print("")

    def part1(self):
        reals = [c.real for c in self.grid.keys() if self.grid[c] != 0]
        imags = [c.imag for c in self.grid.keys() if self.grid[c] != 0]
        intersections = 0
        score = 0
        for y in range(int(min(imags)) - 2, int(max(imags)) + 3):
            for x in range(int(min(reals)) - 2, int(max(reals)) + 3):
                char = self.grid[complex(x, y)]
                if char != "#":
                    continue
                char_n = self.grid[complex(x, y - 1)]
                char_s = self.grid[complex(x, y + 1)]
                char_w = self.grid[complex(x - 1, y)]
                char_e = self.grid[complex(x + 1, y)]
                if char_n == "#" and char_s == "#" and char_w == "#" and char_e == "#":
                    intersections += 1
                    score += x * y

        return score


if __name__ == "__main__":
    program = parse("../../17/input.txt")
    print("Part 1:")
    rd = RepairDroid(program)
    rd.load_pic()
    rd.display()
    print(rd.part1())
    # print(rd.grid)
    # a = rd.execute()
    # print(a)
    # print(Day15.part1(program))
