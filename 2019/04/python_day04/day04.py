#!/usr/bin/env python
def solve(lower, upper):
    return sum(1 for i in range(lower, upper + 1) if is_password(i))
    # return len([i for i in range(lower, upper + 1) if is_password(i)]) # Uses more memory


def solve2(lower, upper):
    return sum(1 for i in range(lower, upper + 1) if is_password2(i))


def is_6digit(cand):
    return cand >= 100000 and cand <= 999999


def is_password(cand):
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
    if not is_6digit(cand):
        return False

    last_num = None
    seen_count = 0
    counts = []  # If number if "155544", counts will be [1, 3, 2]
    for this_num in map(int, str(cand)):
        if last_num is not None and this_num < last_num:
            return False
        if this_num == last_num:
            seen_count += 1
        else:
            if last_num is not None:
                counts.append(seen_count + 1)
            seen_count = 0
        last_num = this_num
    counts.append(seen_count + 1)

    return 2 in counts


if __name__ == "__main__":
    print("Part1: ")
    print(solve(245182, 790572))
    print("Part2: ")
    print(solve2(245182, 790572))
