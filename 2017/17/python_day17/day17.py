#!/usr/bin/env python

from blist import blist


def spin_p1(skip, max_value):
    nums = blist([0])
    loc = 0
    last_loc = 0
    for i in range(1, max_value + 1):
        loc += 1
        nums.insert(loc, i)
        last_loc = loc
        loc = (loc + skip) % len(nums)
    return nums[last_loc + 1]


def spin_p2(skip, max_value):
    nums = blist([0])
    loc = 0
    for i in range(1, max_value + 1):
        loc += 1
        nums.insert(loc, i)
        loc = (loc + skip) % len(nums)
    return nums[1]


if __name__ == "__main__":
    print("Example Part 1: ")
    print(spin_p1(3, 2017))
    print("Real Part 1: ")
    print(spin_p1(304, 2017))
    print("Real Part 2: ")
    print(spin_p2(304, 50_000_000))
