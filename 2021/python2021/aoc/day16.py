#!/usr/bin/env python
"""
Advent Of Code 2021 Day 16
https://adventofcode.com/2021/day/8
"""
from typing import List
import re
from collections import defaultdict
from itertools import islice
import math


def parse(filename: str):
    with open(filename) as file:
        return file.read().strip()
        source_bytes = bytes.fromhex(data)
        return source_bytes


def bits(byte_str):
    for byte in byte_str:
        for i in reversed(range(8)):
            yield (byte >> i) & 1


def take(n, iterable):
    return list(islice(iterable, n))


def to_int(bits):
    answer = 0
    for bit in bits:
        answer *= 2
        answer += bit
    return answer


def version_sum(all_bits):
    bit_stream = iter(all_bits)
    vsum = 0

    packet_version = to_int(take(3, bit_stream))
    packet_type_id = to_int(take(3, bit_stream))
    print("")
    print(f"version {packet_version}")
    print(f"type id {packet_type_id}")
    vsum += packet_version

    if packet_type_id == 4:  # Literal Number
        literal_number = []
        while True:
            first = take(1, bit_stream)
            if first[0] == 1:
                # not last
                literal_number += take(4, bit_stream)
            elif first[0] == 0:
                # last
                literal_number += take(4, bit_stream)
                print(literal_number)
                literal_number = to_int(literal_number)
                # We could consume the padding 0s here
                ## How many padding zeros to run out?

                # for _zero_ in bit_stream:
                #     pass

                break
        print(literal_number)
    else:  # Operator
        first = take(1, bit_stream)  # Length Type ID
        if len(first) == 0:
            pass
        elif first[0] == 0:
            # the next 15 bits are a number that represents the total
            # length in bits
            sub_packet_length = to_int(take(15, bit_stream))
            print(f"sub_packet_length {sub_packet_length}")
            sub_packet_data = take(
                sub_packet_length, bit_stream
            )  # don't know how to split
            print("-->")
            vsum += version_sum(sub_packet_data)
            print("<--")

            ## How many padding zeros to run out?
            # for _zero_ in bit_stream:
            #     pass

        elif first[0] == 1:
            # the next 11 bits are a number that represents the number of
            # sub-packets immediately contained by this packet.
            sub_packet_num = to_int(take(11, bit_stream))
            print(f"sub_packet_num {sub_packet_num}")
            for i in range(sub_packet_num):
                print(f"Looking at subpacket {i}")
                sub_packet_data = list(bit_stream)
                print(sub_packet_data)
                vsum += version_sum(sub_packet_data)

    leftover = list(bit_stream)
    # This is the wrong way to recurse and needs to be rewritten lol
    if len(leftover) > 0:
        print("I was about to return a vsum, but there could be another packet in me!")
        vsum += version_sum(leftover)
    return vsum


def p2(all_bits):
    bit_stream = iter(all_bits)
    results = []
    i = 0

    packet_version = to_int(take(3, bit_stream))
    i += 3
    packet_type_id = to_int(take(3, bit_stream))
    i += 3

    if packet_type_id == 4:  # Literal Number
        literal_number = []
        while True:
            first = take(1, bit_stream)
            i += 1
            if first[0] == 1:
                # not last
                literal_number += take(4, bit_stream)
                i += 4
            elif first[0] == 0:
                # last
                literal_number += take(4, bit_stream)
                i += 4
                break
        results.append(to_int(literal_number))
    else:  # Operator
        first = take(1, bit_stream)  # Length Type ID
        i += 1
        sub_nums = []
        if first[0] == 0:
            # the next 15 bits are a number that represents the total
            # length in bits
            sub_packet_length = to_int(take(15, bit_stream))
            i += 15
            sub_packet_data = take(
                sub_packet_length, bit_stream
            )
            i += sub_packet_length
            j = 0
            while j < sub_packet_length:
                this_nums, this_j = p2(sub_packet_data)
                sub_nums += this_nums
                sub_packet_data = sub_packet_data[this_j:]
                j += this_j
        elif first[0] == 1:
            # the next 11 bits are a number that represents the number of
            # sub-packets immediately contained by this packet.
            sub_packet_num = to_int(take(11, bit_stream))
            i += 11
            sub_packet_data = list(bit_stream)
            for sbi in range(sub_packet_num):
                this_num, this_j = p2(sub_packet_data)
                sub_nums += this_num
                i += this_j
                sub_packet_data = sub_packet_data[this_j:]

        # Collapse numbers
        value = None
        if packet_type_id == 0:
            value = sum(sub_nums)
        elif packet_type_id == 1:
            value = math.prod(sub_nums)
        elif packet_type_id == 2:
            value = min(sub_nums)
        elif packet_type_id == 3:
            value = max(sub_nums)
        elif packet_type_id == 5:
            value = 1 if sub_nums[0] > sub_nums[1] else 0
        elif packet_type_id == 6:
            value = 1 if sub_nums[0] < sub_nums[1] else 0
        elif packet_type_id == 7:
            value = 1 if sub_nums[0] == sub_nums[1] else 0
        results.append(value)

    return results, i


class Day16:
    """ AoC 2021 Day 16 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 16 part 1 """
        data = parse(filename)
        all_bits = list(bits(data))
        print(all_bits)
        return version_sum(all_bits)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 16 part 2 """
        data = parse(filename)
        return Day16.part2_hexstring(data)

    @staticmethod
    def part2_hexstring(hexstring: str) -> int:
        bytestr = bytes.fromhex(hexstring)
        all_bits = list(bits(bytestr))
        results, _i = p2(all_bits)
        return results[0]
