#!/usr/bin/env python
"""
Advent Of Code 2021 Day 16
https://adventofcode.com/2021/day/8
"""
from itertools import islice
import math


def parse(filename: str):
    with open(filename) as file:
        return file.read().strip()


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


def p2(all_bits):
    bit_stream = iter(all_bits)
    results = []
    vsum = 0
    i = 0

    packet_version = to_int(take(3, bit_stream))
    i += 3
    packet_type_id = to_int(take(3, bit_stream))
    i += 3
    vsum += packet_version

    if packet_type_id == 4:  # Literal Number
        literal_number = []
        while True:
            first = take(1, bit_stream)
            i += 1
            literal_number += take(4, bit_stream)
            i += 4
            if first[0] == 0:
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
            sub_packet_data = take(sub_packet_length, bit_stream)
            i += sub_packet_length
            j = 0
            while j < sub_packet_length:
                this_nums, this_j, this_vsum = p2(sub_packet_data)
                sub_nums += this_nums
                sub_packet_data = sub_packet_data[this_j:]
                vsum += this_vsum
                j += this_j
        elif first[0] == 1:
            # the next 11 bits are a number that represents the number of
            # sub-packets immediately contained by this packet.
            sub_packet_num = to_int(take(11, bit_stream))
            i += 11
            sub_packet_data = list(bit_stream)
            for _ in range(sub_packet_num):
                this_num, this_j, this_vsum = p2(sub_packet_data)
                sub_nums += this_num
                i += this_j
                vsum += this_vsum
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

    return results, i, vsum


class Day16:
    """ AoC 2021 Day 16 """

    @staticmethod
    def part1(filename: str) -> int:
        return Day16.part1_hexstring(parse(filename))

    @staticmethod
    def part1_hexstring(hexstring: str) -> int:
        bytestr = bytes.fromhex(hexstring)
        _results, _i, vsum = p2(bits(bytestr))
        return vsum

    @staticmethod
    def part2(filename: str) -> int:
        return Day16.part2_hexstring(parse(filename))

    @staticmethod
    def part2_hexstring(hexstring: str) -> int:
        bytestr = bytes.fromhex(hexstring)
        results, _i, _vsum = p2(bits(bytestr))
        return results[0]
