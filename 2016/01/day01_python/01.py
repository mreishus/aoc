#!/usr/bin/env python
from collections import defaultdict

DIRECTIONS = ["north", "east", "south", "west"]


def turn_right(this_dir_i):
    return (this_dir_i + 1) % len(DIRECTIONS)


def turn_left(this_dir_i):
    return (this_dir_i - 1) % len(DIRECTIONS)


def move(location, dir_i):
    direction = DIRECTIONS[dir_i]
    if direction == "north":
        return location + complex(0, 1)
    if direction == "east":
        return location + complex(1, 0)
    if direction == "south":
        return location + complex(0, -1)
    if direction == "west":
        return location + complex(-1, 0)
    raise Exception("move: Unknown Direction")


def parse(filename):
    return [parse_step(step) for step in open(filename).readline().strip().split(", ")]


def parse_step(step):
    direction = step[0]
    distance = int(step[1:])
    return (direction, distance)


def manhattan(coord):
    return abs(coord.real) + abs(coord.imag)


def solve(steps):
    dir_i = 0  # Start Looking North
    location = complex(0, 0)
    seen = defaultdict(lambda: 0)
    answer2 = None
    for (direction, distance) in steps:
        if direction == "R":
            dir_i = turn_right(dir_i)
        elif direction == "L":
            dir_i = turn_left(dir_i)
        else:
            raise Exception("solve: Unknown Direction")
        for _ in range(distance):
            location = move(location, dir_i)
            seen[location] += 1
            if seen[location] == 2 and answer2 is None:
                answer2 = int(manhattan(location))
    answer1 = int(manhattan(location))
    return answer1, answer2


# data = parse("../input_small.txt")
# data = parse("../input_small2.txt")
# data = parse("../input_small3.txt")
data = parse("../input.txt")
answer1, answer2 = solve(data)
print("Part 1:")
print(answer1)
print("Part 2:")
print(answer2)
