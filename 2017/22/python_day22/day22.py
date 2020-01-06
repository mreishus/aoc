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
            self.direction *= complex(0, -1)  # Turn left
            self.grid[self.virus] = "#"
            self.infection_count += 1
        elif under == "#":
            # Dirty
            self.direction *= complex(0, 1)  # Turn right
            self.grid[self.virus] = "."
        else:
            raise ValueError("Square is neither clean nor dirty")
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
    d22 = Day22("../input.txt")
    print(d22.grid)
    # d22.display()
    for i in range(10_000):
        d22.step()
    d22.display()
    print("")
    print(d22.infection_count)
