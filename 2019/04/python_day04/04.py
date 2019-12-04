#!/usr/bin/env python
from collections import defaultdict

# def parse(filename):
#     return [parse_line(line) for line in open(filename).readlines()]

# def parse_line(line):
#     return "5"

def solve(lower, upper):
    count = 0
    for i in range(lower, upper+1):
        if is_password(i):
            count += 1
    return count

def solve2(lower, upper):
    count = 0
    for i in range(lower, upper+1):
        if is_password2(i):
            count += 1
    return count

def is_password(cand):
    c1 = cand >= 100000 and cand <= 999999
    if not c1:
        return False

    cand_s = str(cand)
    last_num = 0
    seen_double = False
    for element_s in cand_s:
        this_num = int(element_s)
        if this_num < last_num:
            return False
        if this_num == last_num:
            seen_double = True
        last_num = this_num
    return seen_double

def is_password2(cand):
    c1 = cand >= 100000 and cand <= 999999
    if not c1:
        return False

    cand_s = str(cand)
    last_num = 0
    seen_double = False
    seen_count = 0
    counts = []
    for element_s in cand_s:
        this_num = int(element_s)
        if this_num < last_num:
            return False
        if this_num == last_num:
            seen_double = True
            seen_count += 1
        else:
            counts.append(seen_count + 1)
            seen_count = 0
        last_num = this_num
    counts.append(seen_count + 1)
    counts.pop(0)

    return seen_double and 2 in counts




# print(is_password(111111))
# print(is_password(223450))
# print(is_password(123789))
print(is_password2(112233))
print(is_password2(124444))
print(is_password2(111122))

for i in [111122, 123444, 123455, 112344, 113334]:
    print(f" i[{i}] {is_password2(i)}")

# data = parse("../input.txt")

# print(solve(245182, 790572))
# # You guessed 80.
# # You guessed 615.
print(solve2(245182, 790572))

#print(solve(111111, 111113))
