from collections import defaultdict
from os import system
from aoc.computer import Computer

COMPLEX_OF_DIR = {
    "U": complex(0, -1),
    "R": complex(1, 0),
    "D": complex(0, 1),
    "L": complex(-1, 0),
}


def turn(direction, n):
    directions = list(COMPLEX_OF_DIR.keys())
    new_index = (directions.index(direction) + n) % len(directions)
    return directions[new_index]


def turn_right(direction):
    return turn(direction, 1)


def turn_left(direction):
    return turn(direction, -1)


class PainterRobot(object):
    def __init__(self, program):
        self.program = program

    def run_and_return_grid(self, *, initial_color=0):
        cpu = Computer(self.program, [])
        grid = defaultdict(lambda: 0)
        location = complex(0, 0)
        direction = "U"
        grid[location] = initial_color
        # Input to program: 0 if over black (.) , 1 if over white (#)
        # Outputs two values: color to paint 0/black/. 1/white/#, then 0 = turn left, 1 = turn right
        while True:
            current_square = grid[location]
            cpu.add_input(current_square)
            cpu.execute()
            if cpu.state == "halted":
                break
            paint_color = cpu.pop_output()
            turn_dir = cpu.pop_output()
            grid[location] = paint_color
            if turn_dir == 1:
                direction = turn_right(direction)
            elif turn_dir == 0:
                direction = turn_left(direction)
            else:
                raise "Told to turn an invalid direction"
            location += COMPLEX_OF_DIR[direction]
        return grid

    @staticmethod
    def part1(program_in, *, initial_color=0):
        robot = PainterRobot(program_in)
        grid = robot.run_and_return_grid(initial_color=initial_color)
        return len(list(grid.keys()))

    @staticmethod
    def part2(program_in):
        robot = PainterRobot(program_in)
        grid = robot.run_and_return_grid(initial_color=1)
        for y in range(-3, 7):
            for x in range(-5, 45):
                value = grid[complex(x, y)]
                if value == 1:
                    print("#", end="")
                else:
                    print(" ", end="")
            print("")
        return "Look above ^"
