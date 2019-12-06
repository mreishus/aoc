#!/usr/bin/env python


def parse(filename):
    return [parse_line(line.strip()) for line in open(filename).readlines()]


def parse_line(line):
    return line.split(")")


def get_parents(data):
    parent_of = {}
    for pair in data:
        parent_of[pair[1]] = pair[0]
    return parent_of


def part1(parent_of):
    return sum(total_orbits(key, parent_of) for key in parent_of)


def total_orbits(item, parent_of):
    count = 0
    while item in parent_of:
        count += 1
        item = parent_of[item]
    return count


def part2(parent_of):
    p1 = parent_of["YOU"]
    p2 = parent_of["SAN"]
    steps = 0
    while p1 != p2:
        p1_count = total_orbits(p1, parent_of)
        p2_count = total_orbits(p2, parent_of)
        if p1_count > p2_count:
            p1 = parent_of[p1]
            steps += 1
        else:
            p2 = parent_of[p2]
            steps += 1
    return steps


if __name__ == "__main__":
    raw_data = parse("../input.txt")
    parents = get_parents(raw_data)
    p1 = part1(parents)
    p2 = part2(parents)
    print("Part1: ")
    print(p1)
    print("Part2: ")
    print(p2)
