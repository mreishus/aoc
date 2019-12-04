#!/usr/bin/env python
from collections import Counter


def solve(lower, upper):
    """ Given a range of numbers, how many fufill is_password? """
    return sum(1 for i in range(lower, upper + 1) if is_password(i))
    # return len([i for i in range(lower, upper + 1) if is_password(i)]) # Uses more memory


def solve2(lower, upper):
    """ Given a range of numbers, how many fufill is_password2? """
    return sum(1 for i in range(lower, upper + 1) if is_password2(i))


def is_6digit(cand):
    """ Is this number 6 digits long? """
    return 100000 <= cand <= 999999


def is_password(cand):
    """ password: A six digit number, where each digit is monotonically increasing,
    with at least one pair of consecutive numbers. """
    if not is_6digit(cand):
        return False

    last_num = 0
    seen_double = False
    for this_num in map(int, str(cand)):
        if this_num < last_num:
            return False
        if this_num == last_num:
            seen_double = True
        last_num = this_num
    return seen_double


def is_password2(cand):
    """ password2: A six digit number, where each digit is monotonically increasing,
    with at least one pair of consecutive numbers that is exactly 2 digits long.
    Three or more consecutive digits does not count toward the pair requirement. """
    if not is_6digit(cand):
        return False

    # Look for a count of exactly 2 of a digit
    # This works because of the monotonically increasing requirement. An alternative
    # implementation is a run-length encoding, see git history.
    cnt = Counter()
    last_num = None
    for this_num in map(int, str(cand)):
        if last_num is not None and this_num < last_num:
            return False
        cnt[this_num] += 1
        last_num = this_num

    return 2 in cnt.values()


if __name__ == "__main__":
    print("Part1: ")
    print(solve(245182, 790572))
    print("Part2: ")
    print(solve2(245182, 790572))
