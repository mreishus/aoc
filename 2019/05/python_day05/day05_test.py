#!/usr/bin/env python
from unittest import TestCase, main
from day05 import add_one, decode, solve1, parse


class Day05TestCase(TestCase):
    def test_fourdigit(self):
        want = (0, 1, 2, 34)
        got = decode(1234)
        self.assertEqual(want, got)

    def test_fivedigit(self):
        want = (1, 2, 3, 45)
        got = decode(12345)
        self.assertEqual(want, got)
        # (a, b, c, de) = decode(1234)
        # self.assertEqual(a, 1)
        # z = decode(99999)
        # print(z)

    def test_onedigit(self):
        want = (0, 0, 0, 1)
        got = decode(1)
        self.assertEqual(want, got)

    def test_part1(self):
        file_data = parse("../input.txt")
        got = solve1(file_data, 1)
        want = 5821753
        self.assertEqual(want, got)

    def test_8_1(self):
        program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        got = solve1(program, 8)
        want = 1
        self.assertEqual(want, got)
        got = solve1(program, 7)
        want = 0
        self.assertEqual(want, got)
        got = solve1(program, 9)
        want = 0
        self.assertEqual(want, got)

    def test_8_2(self):
        program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        got = solve1(program, 8)
        want = 0
        self.assertEqual(want, got)
        got = solve1(program, 7)
        want = 1
        self.assertEqual(want, got)
        got = solve1(program, 9)
        want = 0
        self.assertEqual(want, got)

    def test_8_3(self):
        program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        got = solve1(program, 8)
        want = 1
        self.assertEqual(want, got)
        got = solve1(program, 7)
        want = 0
        self.assertEqual(want, got)
        got = solve1(program, 9)
        want = 0
        self.assertEqual(want, got)

    def test_8_4(self):
        program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        got = solve1(program, 8)
        want = 0
        self.assertEqual(want, got)
        got = solve1(program, 7)
        want = 1
        self.assertEqual(want, got)
        got = solve1(program, 9)
        want = 0
        self.assertEqual(want, got)

    def test_jump_1(self):
        program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
        got = solve1(program, 0)
        want = 0
        self.assertEqual(want, got)
        got = solve1(program, 10)
        want = 1
        self.assertEqual(want, got)

    def test_jump_2(self):
        program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
        got = solve1(program, 0)
        want = 0
        self.assertEqual(want, got)
        got = solve1(program, 10)
        want = 1
        self.assertEqual(want, got)

    def test_larger(self):
        program = [
            3,
            21,
            1008,
            21,
            8,
            20,
            1005,
            20,
            22,
            107,
            8,
            21,
            20,
            1006,
            20,
            31,
            1106,
            0,
            36,
            98,
            0,
            0,
            1002,
            21,
            125,
            20,
            4,
            20,
            1105,
            1,
            46,
            104,
            999,
            1105,
            1,
            46,
            1101,
            1000,
            1,
            20,
            4,
            20,
            1105,
            1,
            46,
            98,
            99,
        ]
        got = solve1(program, 2)
        want = 999
        self.assertEqual(want, got)
        got = solve1(program, 8)
        want = 1000
        self.assertEqual(want, got)
        got = solve1(program, 12)
        want = 1001
        self.assertEqual(want, got)


if __name__ == "__main__":
    main()
