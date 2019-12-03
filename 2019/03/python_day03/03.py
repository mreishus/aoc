#!/usr/bin/env python
from collections import defaultdict

DIRECTIONS = {
    "R": complex(1, 0),
    "L": complex(-1, 0),
    "U": complex(0, 1),
    "D": complex(0, -1),
}


# filename -> [ wires ]
# wire example: [ ("U", 5), ("D", 40), ... ]
def parse(filename):
    return [parse_line(line) for line in open(filename).readlines()]


# string -> wire
# wire example: [ ("U", 5), ("D", 40), ... ]
def parse_line(line):
    return [parse_step(step) for step in line.strip().split(",")]


# string -> step
# step example: ("R", 10)
def parse_step(step):
    direction = step[0]
    distance = int(step[1:])
    return (direction, distance)


def manhattan(coord):
    return abs(coord.real) + abs(coord.imag)


def solve(wires):
    grid_wire_ids = defaultdict(list)
    grid_steps = defaultdict(list)
    wire_id = 0
    for wire in wires:
        wire_id += 1
        steps = 0
        location = complex(0, 0)
        for (direction, distance) in wire:
            for _ in range(distance):
                location += DIRECTIONS[direction]
                steps += 1
                if wire_id not in grid_wire_ids[location]:
                    grid_wire_ids[location].append(wire_id)
                    grid_steps[location].append(steps)

    intersections = [coord for coord in grid_wire_ids if len(grid_wire_ids[coord]) > 1]
    answer1 = int(min(manhattan(coord) for coord in intersections))
    answer2 = min(sum(grid_steps[coord]) for coord in intersections)
    return (answer1, answer2)


data = parse("../input.txt")
print(solve(data))
