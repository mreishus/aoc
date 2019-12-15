"""
Breakout: Module for playing breakout game in 
Advent of Code 2019 day 15.

Usage example:

from aoc.breakout import Breakout

program = parse("../../13/input.txt")
print("Part 1:")
print(Breakout.part1(program))
print("Part 2:")
# print(Breakout.part2(program, display_to_screen=True))
print(Breakout.part2(program))
"""

from os import system
from collections import defaultdict
from aoc.computer import Computer


class Breakout:
    def __init__(self, program_in):
        self.program = program_in
        self.cpu = Computer(self.program, [])
        self.grid = defaultdict(lambda: 0)

    def input(self, val):
        self.cpu.add_input(val)

    def add_quarters(self):
        self.cpu.memory[0] = 2

    def run_and_return_grid(self):
        cpu = self.cpu
        self.cpu.memory[0] = 2
        grid = self.grid

        cpu.execute()
        while cpu.has_output():
            x = cpu.pop_output()
            y = cpu.pop_output()
            what = cpu.pop_output()
            grid[complex(x, y)] = what

        return grid

    def is_halted(self):
        return self.cpu.is_halted()

    def display(self):
        system("clear")
        for y in range(25):
            for x in range(45):
                char = self.grid[complex(x, y)]
                print_char = " "
                if char == 1:
                    print_char = "W"
                elif char == 2:
                    print_char = "B"
                elif char == 3:
                    print_char = "="
                elif char == 4:
                    print_char = "*"
                print(print_char, end="")
            print("")
        print(f"Score {self.grid[complex(-1, 0)]}")

    def score(self):
        return self.grid[complex(-1, 0)]

    def get_move(self):
        grid = self.grid
        ball = list(grid.keys())[list(grid.values()).index(4)]
        ball_x = int(ball.real)
        paddle = list(grid.keys())[list(grid.values()).index(3)]
        paddle_x = int(paddle.real)
        if ball_x > paddle_x:
            return "r"
        if ball_x < paddle_x:
            return "l"
        return "."

    @staticmethod
    def part1(program_in):
        robot = Breakout(program_in)
        grid = robot.run_and_return_grid()
        return list(grid.values()).count(2)

    @staticmethod
    def part2(program_in, *, display_to_screen=False):
        robot = Breakout(program_in)
        grid = robot.run_and_return_grid()
        robot.add_quarters()
        if display_to_screen:
            robot.display()
        while True:
            a = robot.get_move()
            if a == "l":
                robot.input(-1)
            elif a == "r":
                robot.input(1)
            else:
                robot.input(0)
            if robot.is_halted():
                break
            grid = robot.run_and_return_grid()
            if display_to_screen:
                robot.display()
        return robot.score()
