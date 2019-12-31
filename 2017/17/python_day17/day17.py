#!/usr/bin/env python

from blist import blist


def spin_p1(skip, max_value):
    """ Part 1 using simulated spinlock.
    Insert values from 0 to max_value (inclusive) in the spin-lock,
    then return the number just after the last one inserted. """
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
    """ Part 2 using simulated spinlock.
    Insert values from 0 to max_value (inclusive) in the spin-lock,
    then return the number just after 0.  0 is always first, so
    always return nums[1].
    Runs in 45 seconds with blist.  Will probably never finish with list.
    """
    nums = blist([0])
    loc = 0
    for i in range(1, max_value + 1):
        loc += 1
        nums.insert(loc, i)
        loc = (loc + skip) % len(nums)
    return nums[1]


def spin_p2_fast(skip, max_value):
    """ Part 2 without simulating the entire spinlock.  We don't need to know
    the rest of the values in the spinlock, so we don't bother with them.  We
    do the spinlock simulation, without actually inserting the values.  We
    simply check to see if we're ever inserting at position = 1, and if so,
    save that as our 'last valid answer'.
    Runs much faster: 5 seconds instead of 45 seconds.
    """
    loc = 0
    len_nums = 1
    answer = -1
    for i in range(1, max_value + 1):
        loc += 1
        # We would normally insert at loc right here
        # Mark the answer if we insert at location 1, right after 0
        if loc == 1:
            answer = i
        len_nums += 1
        loc = (loc + skip) % len_nums
    return answer


if __name__ == "__main__":
    print("Example Part 1: ")
    print(spin_p1(3, 2017))
    print("Real Part 1: ")
    print(spin_p1(304, 2017))
    print("Real Part 2: ")
    print(spin_p2_fast(304, 50_000_000))
