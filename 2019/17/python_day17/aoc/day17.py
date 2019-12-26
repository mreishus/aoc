from collections import defaultdict
from os import system
from aoc.computer import Computer

COMPLEX_OF_ROBOTCHAR = {
    "^": complex(0, -1),
    ">": complex(1, 0),
    "v": complex(0, 1),
    "<": complex(-1, 0),
}


def turn_right(direction):
    return direction * complex(0, 1)


def turn_left(direction):
    return direction * complex(0, -1)


def gen_coords(grid):
    """ Given a dictionary with keys as complex numbers representing
    coorindates, return a generator iterating over all coordinates in x, y
    format.  Assumes the grid is not sparse. """
    reals = [c.real for c in grid.keys()]
    imags = [c.imag for c in grid.keys()]
    for y in range(int(min(imags)), int(max(imags)) + 1):
        for x in range(int(min(reals)), int(max(reals)) + 1):
            yield x, y


class Day17Droid:
    def __init__(self, program):
        self.program = program
        self.cpu = Computer(self.program, [])
        self.grid = defaultdict(lambda: 0)
        self.load_pic()

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

    def trace_path(self):
        # print("Trace")
        location, direct = self.robot_location()
        steps = []
        steps_taken = 0
        while True:
            if self.grid[location + direct] != "#":
                # print(f"Need to turn {x} {y}")
                if self.grid[location + turn_right(direct)] == "#":
                    steps.append(steps_taken)
                    steps_taken = 0
                    steps.append("R")
                    direct = turn_right(direct)
                elif self.grid[location + turn_left(direct)] == "#":
                    steps.append(steps_taken)
                    steps_taken = 0
                    steps.append("L")
                    direct = turn_left(direct)
                else:
                    steps.append(steps_taken)
                    # print("Done!")
                    break
            else:
                location += direct
                steps_taken += 1

        # Drop first 0
        steps.pop(0)
        steps2 = []
        while len(steps) > 0:
            turn = str(steps.pop(0))
            how_far = str(steps.pop(0))
            steps2.append(turn + how_far)

        return steps2

    # Is there a better way?
    def is_sublist(self, needle, haystack):
        return self.to_str_comma(needle) in self.to_str_comma(haystack)

    def to_str_comma(self, a):
        return ",".join([str(x) for x in a])

    def create_program(self):
        trace = self.trace_path()
        # print("==========")
        # print(trace)
        # print("==========")

        patterns = {}
        pattern_names = ["A", "B", "C"]
        for n in pattern_names:
            patterns[n] = []

            for i, item in enumerate(trace):
                if item in pattern_names:
                    if len(patterns[n]) > 0:
                        break
                    continue
                patterns[n].append(item)
                pattern_length = sum(len(x) + 2 for x in patterns[n]) - 1
                if pattern_length > 20 or not self.is_sublist(
                    patterns[n], trace[i + 1 :]
                ):
                    patterns[n].pop()
                    break

            p_str = self.to_str_comma(patterns[n])
            trace_str = self.to_str_comma(trace)
            trace = trace_str.replace(p_str, n).split(",")

        prog = ",".join(trace) + "\n"
        for p in patterns.values():
            prog += ",".join(p).replace("R", "R,").replace("L", "L,") + "\n"

        everything = self.prog_to_ascii(prog) + self.prog_to_ascii("n\n")
        return everything

    def prog_to_ascii(self, string):
        return [ord(s) for s in string]

    def robot_location(self):
        location = complex(-1, -1)
        robot_char = ""
        for x, y in gen_coords(self.grid):
            char = self.grid[complex(x, y)]
            if char == "^" or char == "v" or char == "<" or char == ">":
                location = complex(x, y)
                robot_char = char
                break

        return location, COMPLEX_OF_ROBOTCHAR[robot_char]

    def part1(self):
        intersections = 0
        score = 0
        for x, y in gen_coords(self.grid):
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

    def part2(self):
        prog = self.create_program()

        # Load prog into computer, execute
        cpu = Computer(self.program, [])
        cpu.memory[0] = 2
        for instruction in prog:
            cpu.add_input(instruction)
        cpu.execute()
        result = []
        while cpu.has_output():
            result.append(cpu.pop_output())
        return result[-1]
