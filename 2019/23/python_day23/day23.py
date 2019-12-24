#!/usr/bin/env python

from collections import defaultdict, deque
from aoc.computer import Computer, solve1
from aoc.day21 import Day21


def parse(filename):
    with open(filename) as f:
        return [int(num) for num in f.readline().strip().split(",")]


class Day23:
    def __init__(self, program, how_many=50):
        # Init variables
        self.program = program
        self.how_many = how_many
        self.computers = None
        self.queue_for_address = defaultdict(deque)
        # Create computers
        self.spawn_computers()

    def spawn_computers(self):
        computers = []
        for i in range(self.how_many):
            cpu = Computer(self.program, [i])
            computers.append(cpu)
        self.computers = computers

    def execute(self):
        done = False
        p1_answer = None
        while not done:
            for address in range(self.how_many):
                cpu = self.computers[address]

                if len(self.queue_for_address[address]) > 0:
                    (x, y) = self.queue_for_address[address].popleft()
                    cpu.add_input(x)
                    cpu.add_input(y)
                else:
                    cpu.add_input(-1)

                cpu.execute()
                if cpu.len_output() >= 3:
                    address = cpu.pop_output()
                    x = cpu.pop_output()
                    y = cpu.pop_output()
                    self.queue_for_address[address].append((x, y))

                if len(self.queue_for_address[255]) > 0:
                    (x, y) = self.queue_for_address[255].popleft()
                    p1_answer = y
                    done = True
                    break

        return p1_answer


if __name__ == "__main__":
    program = parse("../../23/input.txt")
    d23 = Day23(program)
    p1 = d23.execute()
    print("part 1")
    print(p1)
    # print(d21.part1())
    # print("part 2")
    # print(d21.part2())
