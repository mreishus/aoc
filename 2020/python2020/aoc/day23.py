#!/usr/bin/env python
"""
Advent Of Code 2020 Day 23
https://adventofcode.com/2020/day/23
"""

from typing import List


def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip()
        x = []
        for char in lines:
            x.append(int(char))
        return x


class Node:
    def __init__(self, data=0, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        if self.next is None:
            return f"Node[{self.data}] -> None"
        else:
            return f"Node[{self.data}] -> ?"


## Input: [5, 2, 3, 4]
## Output: Node(5) -> Node(2) -> Node(3) -> Node(4) -> (beginning entry, for infinite loop)
def build_linked_list(cup_names):
    first_node = None
    last_node = None

    # Build infinite linked list
    for cup in cup_names:
        node = Node(cup)
        if first_node is None:
            first_node = node
        if last_node is not None:
            last_node.next = node
        last_node = node

    last_node.next = first_node
    return first_node


def p1(cup_names: List[int]):
    current, nodes_by_num = do_it(cup_names, 100)

    # Starting after the cup labeled 1, collect the other cups' labels clockwise
    # into a single string with no extra characters
    current = nodes_by_num[1]
    current = current.next
    result = []
    for i in range(len(cup_names) - 1):
        result.append(str(current.data))
        current = current.next
    return "".join(result)


def p2(cup_names: List[int]):
    fill_to = 1000000
    max_cup = max(cup_names)
    cup_names = cup_names + list(range(max_cup + 1, fill_to + 1))

    current, nodes_by_num = do_it(cup_names, 10000000)

    # Determine which two cups will end up immediately clockwise of cup 1. What
    # do you get if you multiply their labels together?
    current = nodes_by_num[1]
    return current.next.data * current.next.next.data


def do_it(cup_names: List[int], move_num: int):
    min_cup = min(cup_names)
    max_cup = max(cup_names)

    first_cup = build_linked_list(cup_names)
    current = first_cup

    nodes_by_num = {}
    for _ in range(len(cup_names)):
        nodes_by_num[current.data] = current
        current = current.next

    current = first_cup

    #  /--------------v
    # 3 8->9->1->None 2
    # ^ ^Picked_up
    # Current
    for _ in range(move_num):
        # Debug
        # for i in range(len(cup_names)):
        #     print(current.data, end=" ")
        #     current = current.next
        # print(f"Doing move {move_i + 1}")

        # The crab picks up the three cups that are immediately clockwise of the current cup.
        picked_up = current.next
        current.next = current.next.next.next.next
        picked_up.next.next.next = None

        picked_up_vals = set(
            [picked_up.data, picked_up.next.data, picked_up.next.next.data]
        )

        # The crab selects a destination cup: the cup with a label equal to the
        # current cup's label minus one.
        dest_num = current.data - 1
        if dest_num < min_cup:
            dest_num = max_cup
        while dest_num in picked_up_vals:
            dest_num -= 1
            if dest_num < min_cup:
                dest_num = max_cup

        # The crab places the cups it just picked up so that they are
        # immediately clockwise of the destination cup.
        dest = nodes_by_num[dest_num]
        remember_me = dest.next
        dest.next = picked_up
        picked_up.next.next.next = remember_me

        # The crab selects a new current cup: the cup which is immediately
        # clockwise of the current cup.
        current = current.next

    return current, nodes_by_num


class Day23:
    """ AoC 2020 Day 23 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 23 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 23 part 2 """
        data = parse(filename)
        return p2(data)
