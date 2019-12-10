#!/usr/bin/env python
from fractions import Fraction
import math


def parse(filename):
    with open(filename) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def parse_line(line):
    return list(line)


def display(grid):
    for row in grid:
        for char in row:
            print(char, end="")
        print("")


# With my coordinate system
# up and a little left = 359
# up and a little right = 1
# right = 270
# down = 180
# left = 90
def angle(x1, y1, x2, y2):
    return (math.atan2(x2 - x1, y2 - y1) * 180 / math.pi) + 180
    # return (math.atan2(y2 - y1, x2 - x1) * 180 / math.pi) + 180


def part1(grid):
    # display(grid)
    size_y = len(grid)
    size_x = len(grid[0])
    # print(f"{size_x} x {size_y}")

    max_sight = 0
    max_x = 0
    max_y = 0
    for y in range(size_y):
        for x in range(size_x):
            seen, _ = how_many_seen(grid, x, y)
            # print(f"x{x} y{y} seen {seen}")
            if seen > max_sight:
                max_sight = seen
                max_x = x
                max_y = y
    return max_x, max_y, max_sight


def how_many_seen(grid, x, y):
    if grid[y][x] == ".":
        return 0, []
    # Build Blocked dict
    size_y = len(grid)
    size_x = len(grid[0])
    blocked = {}
    for ax in range(size_x):
        for ay in range(size_y):
            if ax == x and ay == y:
                continue
            if grid[ay][ax] == ".":
                continue
            x_diff = ax - x
            y_diff = ay - y
            x_diff_scaled = x_diff
            y_diff_scaled = y_diff
            if x_diff == 0:
                if y_diff_scaled > 0:
                    y_diff_scaled = 1
                else:
                    y_diff_scaled = -1
            elif y_diff == 0:
                if x_diff_scaled > 0:
                    x_diff_scaled = 1
                else:
                    x_diff_scaled = -1
            else:
                slope1 = Fraction(x_diff, y_diff)
                slope2 = Fraction(y_diff, x_diff)
                if abs(slope1.numerator) < abs(x_diff):
                    x_diff_scaled = slope1.numerator
                    y_diff_scaled = slope1.denominator
                elif abs(slope2.numerator) < abs(y_diff):
                    y_diff_scaled = slope1.numerator
                    x_diff_scaled = slope1.denominator
            # -2/-4 reduces to 1/2, we want it to be -1/-2
            # Other sign cases that can go wrong here
            if x_diff < 0 and x_diff_scaled > 0:
                x_diff_scaled *= -1
            if x_diff > 0 and x_diff_scaled < 0:
                x_diff_scaled *= -1
            if y_diff < 0 and y_diff_scaled > 0:
                y_diff_scaled *= -1
            if y_diff > 0 and y_diff_scaled < 0:
                y_diff_scaled *= -1

            # print(f"What does {ax} {ay} block?")
            # print(f"  [{x_diff} {y_diff}] -> [{x_diff_scaled} {y_diff_scaled}]")

            blocked_x = ax
            blocked_y = ay
            while True:
                blocked_x += x_diff_scaled
                blocked_y += y_diff_scaled
                if (
                    blocked_x >= size_x
                    or blocked_x <= -1
                    or blocked_y >= size_y
                    or blocked_y <= -1
                ):
                    break
                # print(f"   --> Blocked!: {blocked_x} {blocked_y}")
                blocked[(blocked_y, blocked_x)] = True

    count = 0
    seen_list = []
    for ax in range(size_x):
        for ay in range(size_y):
            if grid[ay][ax] != "#":
                continue
            if ax == x and ay == y:
                continue
            if (ay, ax) in blocked:
                # print(f"{ax} {ay} is BLOCKED")
                continue
            # print(f" See {ax} {ay}")
            count += 1
            seen_list.append((ax, ay))

    return count, seen_list


def part2(grid):
    deletes = part2_deletes(grid)
    (x, y) = deletes[200 - 1]
    return x * 100 + y


def part2_deletes(grid):
    (station_x, station_y, count) = part1(grid)

    last_ang = 0.00001
    count, seen_list = how_many_seen(grid, station_x, station_y)

    deleted = []

    while True:
        if count == 0:
            break
        del_x, del_y, last_ang = get_next(station_x, station_y, seen_list, last_ang)
        # print(f"{del_x} {del_y} {last_ang}")
        deleted.append((del_x, del_y))
        grid[del_y][del_x] = "."
        count, seen_list = how_many_seen(grid, station_x, station_y)

    return deleted


def get_next(station_x, station_y, seen_list, last_ang):
    seen_list_ang = [(x, y, angle(station_x, station_y, x, y)) for (x, y) in seen_list]
    seen_list_ang.sort(key=lambda x: x[2], reverse=True)
    filtered = list(filter(lambda elem: elem[2] < last_ang, seen_list_ang))

    if len(filtered) > 0:
        return filtered[0]
    return seen_list_ang[0]


if __name__ == "__main__":
    print("Part1: ")
    grid = parse("../input.txt")
    print(part1(grid))

    print("Part 2:")
    grid = parse("../input.txt")
    print(part2(grid))
