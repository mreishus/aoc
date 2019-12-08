#!/usr/bin/env python
import itertools

flatten = itertools.chain.from_iterable


def load(filename, width, height):
    with open(filename, "r") as myfile:
        data = myfile.read().strip()
        # num_planes = len(data) // (width * height)
        x = 0
        y = 0
        z = 0
        row = []
        rows = []
        planes = []
        for char in data:
            row.append(int(char))
            x += 1
            if x >= width:
                rows.append(row)
                row = []
                x = 0
                y += 1
                if y >= height:
                    planes.append(rows)
                    rows = []
                    y = 0
                    z += 1
        print(f"Number of planes: {len(planes)}")
    return planes


def plane_count(plane, target):
    """ Given a plane (2d array) and a target number, how many times
    does that number appear in that plane? """
    flatplane = list(flatten(plane))
    return len([x for x in flatplane if x == target])


def part1(planes):
    plane_min_zeros = min(planes, key=lambda plane: plane_count(plane, 0))
    return plane_count(plane_min_zeros, 1) * plane_count(plane_min_zeros, 2)


def part2(planes):
    num_planes = len(planes)
    num_y = len(planes[0])
    num_x = len(planes[0][0])
    for y in range(num_y):
        for x in range(num_x):
            char = "?"
            for z in range(num_planes):
                this_char = planes[z][y][x]
                if this_char in (0, 1):
                    char = this_char
                    break
            if char == 1:
                print("#", end="")
            elif char == 0:
                print(" ", end="")
            else:
                print(char, end="")
        print("")

    print(f"planes: {num_planes} y: {num_y} x: {num_x}")


if __name__ == "__main__":
    # a1 = load("./input_small.txt", 3, 2)
    a1 = load("../input.txt", 25, 6)
    print("Part1: ")
    print(part1(a1))
    print("Part2: ")
    part2(a1)
