#!/usr/bin/env python


def spin(skip, max_value):
    nums = [0]
    loc = 0
    last_loc = 0
    for i in range(1, max_value + 1):
        loc += 1
        nums.insert(loc, i)
        last_loc = loc
        loc = (loc + skip) % len(nums)
    return nums[last_loc + 1]


if __name__ == "__main__":
    print("Example Part 1: ")
    print(spin(3, 2017))
    print("Real Part 1: ")
    print(spin(304, 2017))
