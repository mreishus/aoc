#!/usr/bin/env python

from collections import defaultdict, deque, Counter
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
        nat_value = None
        idle_last_tick = False
        last_wakeup_y_sent = None
        while not done:
            address_sent_message = Counter()
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
                    address_out = cpu.pop_output()
                    x = cpu.pop_output()
                    y = cpu.pop_output()
                    if address_out == 255:
                        nat_value = (x, y)
                    else:
                        self.queue_for_address[address_out].append((x, y))
                    address_sent_message[address] += 1

                if p1_answer is None and nat_value is not None:
                    (x, y) = nat_value
                    p1_answer = y
                    # done = True
                    # break

                # If idle last rotation and this rotation, send special
                # wakeup message
                idle_this_tick = sum(address_sent_message.values()) == 0
                if idle_last_tick and idle_this_tick and nat_value is not None:
                    (x, y) = nat_value
                    # print(f"Sending {x} {y} Wakeup")

                    address_out = 0
                    self.queue_for_address[address_out].append((x, y))
                    address_sent_message[255] += 1

                    if last_wakeup_y_sent == y:
                        p2_answer = y
                        done = True
                        break
                    last_wakeup_y_sent = y

            idle_last_tick = sum(address_sent_message.values()) == 0

        return p1_answer, p2_answer


if __name__ == "__main__":
    program = parse("../../23/input.txt")
    d23 = Day23(program)
    p1, p2 = d23.execute()
    print("part 1")
    print(p1)
    print("part 2")
    print(p2)
