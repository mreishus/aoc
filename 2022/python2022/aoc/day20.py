#!/usr/bin/env python
"""
Advent Of Code 2022 Day 20
https://adventofcode.com/2022/day/20
"""
from typing import List
from random import randint


def parse(filename: str) -> List[int]:
    with open(filename) as file:
        return [int(line.strip()) for line in file.readlines()]


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None
        self.guid = randint(0, 1000000)

    def __repr__(self):
        return f"Node({self.value}, {self.guid})"


def build_dll(data):
    """Build a doubly linked list from the data"""
    ilookup = {}
    i = 0
    zero = None

    head = Node(data[0])
    ilookup[i] = head
    if data[0] == 0:
        zero = head

    current = head
    for value in data[1:]:
        current.next = Node(value)
        current.next.prev = current
        current = current.next

        i += 1
        ilookup[i] = current

        if value == 0:
            zero = current

    current.next = head
    head.prev = current
    return head, ilookup, zero


def p1(data, mix_amount):
    dll, ilookup, zero = build_dll(data)
    i = 0
    pointer = dll

    for mix_i in range(mix_amount):
        # print("Begin mix", mix_i)
        dll = mix(dll, ilookup)
        # print("Finished mix", mix_i)

    ## Debugger
    # pointer = dll
    # while pointer is not None and i <= len(data):
    #     print(pointer)
    #     prevPointer = pointer
    #     pointer = pointer.next
    #     i += 1

    ## Find 0
    specials = []
    pointer = zero
    for _ in range(3):
        for _ in range(1000):
            pointer = pointer.next
        specials.append(pointer.value)

    return sum(specials)


#             mnp
#   op    c   on
#    2    1    3                 4
#    2         3        1        4
#
#    "Picking up C"
#    op.next = on
#    on.prev = op
#
#    "Inserting C"
#    tmp = mnp.next
#    mnp.next = c
#    c.next = tmp
#    tmp.prev = c
#
#    c.prev = mnp


#              mnn
#              op       c       on
#    2         3        1        4
#    2    1    3                 4
#
#    "Picking up C"
#    op.next = on
#    on.prev = op

#    tmp = mnn.prev
#    mnn.prev = c
#    c.prev = tmp
#    tmp.next = c
#
#    c.next = mnn


def new_mod(a, b):
    """mod that returns negatives"""
    res = a % b
    return res if not res else res - b if a < 0 else res


def mix(dll, ilookup):
    for i in sorted(ilookup.keys()):
        current = ilookup[i]
        value = current.value

        old_prev = current.prev
        old_next = current.next
        my_new_prev = current
        my_new_next = current

        altValue = new_mod(value, len(ilookup) - 1)

        if value > 0:
            old_prev.next = old_next
            old_next.prev = old_prev

            for _ in range(altValue):
                my_new_prev = my_new_prev.next
            if my_new_prev == current:
                my_new_prev = my_new_prev.prev

            tmp = my_new_prev.next
            my_new_prev.next = current
            current.next = tmp
            tmp.prev = current
            current.prev = my_new_prev
        elif value < 0:
            old_prev.next = old_next
            old_next.prev = old_prev

            for _ in range(abs(altValue)):
                my_new_next = my_new_next.prev
            if my_new_next == current:
                my_new_next = my_new_next.next

            tmp = my_new_next.prev
            my_new_next.prev = current
            current.prev = tmp
            tmp.next = current
            current.next = my_new_next
        else:
            continue

    return dll


def debug_view(dll):
    """
    1, 2, -3, 3, -2, 0, 4,  | 4, 0, -2, 3, -3, 2, 1,
    1, -3, 3, -2, 0, 4, 2,  | 2, 4, 0, -2, 3, -3, 1,
    1, -3, 2, 3, -2, 0, 4,  | 4, 0, -2, 3, 2, -3, 1,
    1, 2, 3, -2, -3, 0, 4,  | 4, 0, -3, -2, 3, 2, 1,
    1, 2, -2, -3, 0, 3, 4,  | 4, 3, 0, -3, -2, 2, 1,
    1, 2, -3, 0, 3, 4, -2,  | -2, 4, 3, 0, -3, 2, 1,
    1, 2, -3, 4, 0, 3, -2,  | -2, 3, 0, 4, -3, 2, 1,
    """
    forward = []
    backward = []

    pointer = dll
    while pointer is not None:
        print(pointer.value, end=", ")
        forward.append(pointer.value)

        pointer = pointer.next
        if pointer == dll:
            break
    print(" | ", end="")

    pointer = dll.prev
    while pointer is not None:
        print(pointer.value, end=", ")
        backward.append(pointer.value)

        pointer = pointer.prev
        if pointer == dll.prev:
            break

    if forward != backward[::-1]:
        print("ERROR")
        exit()
    print(len(forward), len(backward))


class Day20:
    """AoC 2022 Day 20"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        return p1(data, 1)

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        data = [x * 811589153 for x in data]
        return p1(data, 10)
