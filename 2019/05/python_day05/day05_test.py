#!/usr/bin/env python
from unittest import TestCase, main
from day05 import solve1, parse, digit_from_right


class Day05TestCase(TestCase):
    def test_digit_from_right(self):
        self.assertEqual(digit_from_right(12345, 0), 5)
        self.assertEqual(digit_from_right(12345, 1), 4)
        self.assertEqual(digit_from_right(12345, 2), 3)
        self.assertEqual(digit_from_right(12345, 3), 2)
        self.assertEqual(digit_from_right(12345, 4), 1)
        self.assertEqual(digit_from_right(12345, 5), 0)
        self.assertEqual(digit_from_right(498, 0), 8)
        self.assertEqual(digit_from_right(498, 1), 9)
        self.assertEqual(digit_from_right(498, 2), 4)
        self.assertEqual(digit_from_right(498, 3), 0)
        self.assertEqual(digit_from_right(498, 4), 0)
        self.assertEqual(digit_from_right(498, 5), 0)

    def test_part1(self):
        file_data = parse("../input.txt")
        got = solve1(file_data, [1])
        want = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5821753]
        self.assertEqual(want, got)

    def test_part2(self):
        file_data = parse("../input.txt")
        got = solve1(file_data, [5])
        want = [11956381]
        self.assertEqual(want, got)

    def test_8_1(self):
        program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        got = solve1(program, [8])
        want = [1]
        self.assertEqual(want, got)
        got = solve1(program, [7])
        want = [0]
        self.assertEqual(want, got)
        got = solve1(program, [9])
        want = [0]
        self.assertEqual(want, got)

    def test_8_2(self):
        program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        got = solve1(program, [8])
        want = [0]
        self.assertEqual(want, got)
        got = solve1(program, [7])
        want = [1]
        self.assertEqual(want, got)
        got = solve1(program, [9])
        want = [0]
        self.assertEqual(want, got)

    def test_8_3(self):
        program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        got = solve1(program, [8])
        want = [1]
        self.assertEqual(want, got)
        got = solve1(program, [7])
        want = [0]
        self.assertEqual(want, got)
        got = solve1(program, [9])
        want = [0]
        self.assertEqual(want, got)

    def test_8_4(self):
        program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        got = solve1(program, [8])
        want = [0]
        self.assertEqual(want, got)
        got = solve1(program, [7])
        want = [1]
        self.assertEqual(want, got)
        got = solve1(program, [9])
        want = [0]
        self.assertEqual(want, got)

    def test_jump_1(self):
        program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
        got = solve1(program, [0])
        want = [0]
        self.assertEqual(want, got)
        got = solve1(program, [10])
        want = [1]
        self.assertEqual(want, got)

    def test_jump_2(self):
        program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
        got = solve1(program, [0])
        want = [0]
        self.assertEqual(want, got)
        got = solve1(program, [10])
        want = [1]
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
        got = solve1(program, [2])
        want = [999]
        self.assertEqual(want, got)
        got = solve1(program, [8])
        want = [1000]
        self.assertEqual(want, got)
        got = solve1(program, [12])
        want = [1001]
        self.assertEqual(want, got)


if __name__ == "__main__":
    main()
