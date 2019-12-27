#!/usr/bin/env python
from functools import reduce


def transform(nums, input_lengths, num_rounds=1):
    pos = 0
    skip_size = 0
    size = len(nums)

    for _ in range(num_rounds):
        for input_length in input_lengths:
            r_begin = pos
            r_end = (pos + (input_length - 1)) % size
            num_swaps = input_length // 2
            for _ in range(num_swaps):
                nums[r_begin], nums[r_end] = nums[r_end], nums[r_begin]
                r_begin = (r_begin + 1) % size
                r_end = (r_end - 1) % size
            pos = (pos + input_length + skip_size) % size
            skip_size += 1

    return nums


def densify(nums):
    i = 0
    output = []
    while i < len(nums):
        this_section = nums[i : i + 16]
        this_answer = reduce((lambda x, y: x ^ y), this_section)
        output.append(this_answer)
        i += 16
    return output


# In: "../input.txt"
# Out: List [230, 1, 2, 3, 97, ... ]
def parse_nums(filename):
    with open(filename) as f:
        string_nums = f.readline().strip().split(",")
        return [int(x) for x in string_nums]


# In: "../input.txt"
# Out: String "230, 1, 2, 3, 97, "
def parse_string(filename):
    with open(filename) as f:
        return f.readline().strip()


def hexify(nums):
    """ Take a list of integers, convert them to hex representations, then
    stick them together in a string.
    hex(x) - Converts 64 to 0x40
    [2:] - Strips off "0x" at the beginning
    .rjust(2, "0") - Adds a leading 0 if one digit
    """
    return "".join(hex(x)[2:].rjust(2, "0") for x in nums)


def string_to_input_nums(string):
    inputs = [ord(x) for x in string]
    inputs += [17, 31, 73, 47, 23]
    return inputs


def part1(length, inputs):
    p1_list = transform(list(range(length)), inputs)
    return p1_list[0] * p1_list[1]


def part2(string):
    inputs = string_to_input_nums(string)
    sparse_hash = transform(list(range(256)), inputs, num_rounds=64)
    dense_hash = densify(sparse_hash)
    hex_string = hexify(dense_hash)
    return hex_string


if __name__ == "__main__":
    print("Part1: ")
    length = 256
    inputs = parse_nums("../input.txt")
    print(part1(length, inputs))

    print("Part 2:")
    print(part2(parse_string("../input.txt")))
