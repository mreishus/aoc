#!/usr/bin/env python3

def parse(filename):
    with open(filename) as f:
        lines = [int(x.strip()) for x in f.readlines()]
        return lines

def part1(jumps):
    jmax = len(jumps)
    current_idx = 0
    old_idx = 0
    steps = 0
    while True:
        old_idx = current_idx
        if current_idx >= jmax:
            break
        current_idx += jumps[current_idx]
        jumps[old_idx] += 1
        steps += 1
    return steps

def part2(jumps):
    jmax = len(jumps)
    current_idx = 0
    old_idx = 0
    steps = 0
    while True:
        old_idx = current_idx
        if current_idx >= jmax:
            break
        current_idx += jumps[current_idx]
        if jumps[old_idx] >= 3:
            jumps[old_idx] -= 1
        else:
            jumps[old_idx] += 1
        steps += 1
    return steps

jumps = parse("../input_small.txt")
p1 = part1(jumps)
print("Expect to see: 5")
print(p1)

## --

jumps = parse("../input_small.txt")
p2 = part2(jumps)
print("Expect to see: 10")
print(p2)

print("\n")

jumps = parse("../input.txt")
p1 = part1(jumps)
print("Part1:")
print(p1)

## --

jumps = parse("../input.txt")
p2 = part2(jumps)
print("Part2:")
print(p2)
