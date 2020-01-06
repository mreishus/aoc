#!/usr/bin/env python

from collections import defaultdict


class Day22:
    def __init__(self, filename):
        self.grid = self._parse(filename)
        self.virus = complex(0, 0)
        self.direction = complex(0, -1)  # Facing up
        self.infection_count = 0

    def _parse(self, filename):
        grid = defaultdict(lambda: ".")
        with open(filename) as file:
            lines = [line.strip() for line in file]
            max_width = len(lines[0].strip())
            start_x = -1 * int(max_width / 2)
            start_y = start_x
            y = start_y

            for line in lines:
                x = start_x
                for char in line:
                    grid[complex(x, y)] = char
                    x += 1
                y += 1
        return grid

    def step(self):
        under = self.grid[self.virus]
        if under == ".":
            # Clean
            self.turn_left()
            self.grid[self.virus] = "#"
            self.infection_count += 1
        elif under == "#":
            # Dirty
            self.turn_right()
            self.grid[self.virus] = "."
        else:
            raise ValueError("Square is neither clean nor dirty")
        self.virus += self.direction

    def turn_right(self):
        self.direction *= complex(0, 1)

    def turn_left(self):
        self.direction *= complex(0, -1)

    def reverse(self):
        self.turn_right()
        self.turn_right()

    def step_part2(self):
        under = self.grid[self.virus]
        if under == ".":
            # Clean -> Weak
            self.turn_left()
            self.grid[self.virus] = "W"
        elif under == "W":
            # Weak -> Infected
            self.grid[self.virus] = "#"
            self.infection_count += 1
        elif under == "#":
            # Infected -> Flagged
            self.turn_right()
            self.grid[self.virus] = "F"
        elif under == "F":
            # Flagged -> Clean
            self.reverse()
            self.grid[self.virus] = "."
        else:
            raise ValueError("Unknown square value")
        # Step Forward
        self.virus += self.direction

    def display(self):
        for y in range(-5, 5):
            print("")
            for x in range(-5, 5):
                if self.virus == complex(x, y):
                    print("V", end="")
                else:
                    print(self.grid[complex(x, y)], end="")


if __name__ == "__main__":
    print("Part 1:")
    d22 = Day22("../input.txt")
    for i in range(10_000):
        d22.step()
    d22.display()
    print("")
    print(d22.infection_count)
    print("")
    print("Part 2:")
    d22 = Day22("../input.txt")
    for i in range(10000000):
        d22.step_part2()
    print(d22.infection_count)
