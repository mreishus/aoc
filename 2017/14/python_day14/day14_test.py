#!/usr/bin/env python
from unittest import TestCase, main

from aoc.day10 import densify, transform, parse_nums, part1, string_to_input_nums, part2


class Day10TestCase(TestCase):
    def test_part1_example(self):
        length = 5
        inputs = [3, 4, 1, 5]
        new_list = transform(list(range(length)), inputs)
        self.assertEqual(new_list, [3, 4, 2, 1, 0])

    def test_part1(self):
        length = 256
        inputs = parse_nums("../../10/input.txt")
        p1_ans = part1(length, inputs)
        self.assertEqual(p1_ans, 2928)

    def test_densify(self):
        copy1 = [65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]
        copy2 = copy1 * 2
        dc1 = densify(copy1)
        dc2 = densify(copy2)
        self.assertEqual(dc1, [64])
        self.assertEqual(dc2, [64, 64])

    def test_string_to_input_nums(self):
        got = string_to_input_nums("1,2,3")
        want = [49, 44, 50, 44, 51, 17, 31, 73, 47, 23]
        self.assertEqual(got, want)

    def test_part2(self):
        got = part2("1,2,3")
        want = "3efbe78a8d82f29979031a4aa0b16a9d"
        self.assertEqual(got, want)

        got = part2("1,2,4")
        want = "63960835bcdc130f0b66d7ff4f6a5a8e"
        self.assertEqual(got, want)

        got = part2("AoC 2017")
        want = "33efeb34ea91902bb2f59c9920caa6cd"
        self.assertEqual(got, want)

        got = part2("")
        want = "a2582a3a0e66e6e86e3812dcb672a272"
        self.assertEqual(got, want)


if __name__ == "__main__":
    main()
