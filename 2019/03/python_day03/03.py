#!/usr/bin/env python
from collections import defaultdict

DIRECTIONS = {
    "R": complex(1, 0),
    "L": complex(-1, 0),
    "U": complex(0, 1),
    "D": complex(0, -1),
}


def parse(filename):
    return [parse_line(line) for line in open(filename).readlines()]


def parse_line(line):
    return [parse_step(step) for step in line.strip().split(",")]


def parse_step(step):
    direction = step[0]
    distance = int(step[1:])
    return (direction, distance)


def manhattan(coord):
    return abs(coord.real) + abs(coord.imag)


def solve(lines):
    grid_line_ids = defaultdict(list)
    grid_steps = defaultdict(list)
    line_id = 0
    for line in lines:
        line_id += 1
        steps = 0
        location = complex(0, 0)
        for (direction, distance) in line:
            for _ in range(distance):
                location += DIRECTIONS[direction]
                steps += 1
                if line_id not in grid_line_ids[location]:
                    grid_line_ids[location].append(line_id)
                    grid_steps[location].append(steps)

    intersections = [
        coord for coord in grid_line_ids.keys() if len(grid_line_ids[coord]) > 1
    ]
    answer1 = int(min([manhattan(coord) for coord in intersections]))
    answer2 = int(min([sum(grid_steps[coord]) for coord in intersections]))
    return (answer1, answer2)


data = parse("../input.txt")
print(solve(data))
