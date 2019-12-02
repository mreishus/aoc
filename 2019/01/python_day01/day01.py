#!/usr/bin/env python

def fuel(num):
    return num // 3 - 2

def total_fuel(f):
    total = 0
    while True:
        f = fuel(f)
        if f <= 0:
            break
        total += f

    return total

def part1(data):
    return sum([fuel(num) for num in data])

def part2(data):
    return sum([total_fuel(num) for num in data])

def main():
    data = [int(line.strip()) for line in open("../input.txt").readlines()]
    print("Part1:")
    print(part1(data))
    print("Part2:")
    print(part2(data))

if __name__ == "__main__":
    main()
