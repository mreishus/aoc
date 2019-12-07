#!/usr/bin/env python
from unittest import TestCase, main

from day07 import (
    parse,
    part1,
    part2,
    amplify_once,
    amplify_once_find_max_seq,
    amplify_loop,
    amplify_loop_max_seq,
)


class Programs7:
    prog_a_1 = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    prog_a_2 = [
        3,
        23,
        3,
        24,
        1002,
        24,
        10,
        24,
        1002,
        23,
        -1,
        23,
        101,
        5,
        23,
        23,
        1,
        24,
        23,
        23,
        4,
        23,
        99,
        0,
        0,
    ]
    prog_a_3 = [
        3,
        31,
        3,
        32,
        1002,
        32,
        10,
        32,
        1001,
        31,
        -2,
        31,
        1007,
        31,
        0,
        33,
        1002,
        33,
        7,
        33,
        1,
        33,
        31,
        31,
        1,
        32,
        31,
        31,
        4,
        31,
        99,
        0,
        0,
        0,
    ]
    prog_b_1 = [
        3,
        26,
        1001,
        26,
        -4,
        26,
        3,
        27,
        1002,
        27,
        2,
        27,
        1,
        27,
        26,
        27,
        4,
        27,
        1001,
        28,
        -1,
        28,
        1005,
        28,
        6,
        99,
        0,
        0,
        5,
    ]
    prog_b_2 = [
        3,
        52,
        1001,
        52,
        -5,
        52,
        3,
        53,
        1,
        52,
        56,
        54,
        1007,
        54,
        5,
        55,
        1005,
        55,
        26,
        1001,
        54,
        -5,
        54,
        1105,
        1,
        12,
        1,
        53,
        54,
        53,
        1008,
        54,
        0,
        55,
        1001,
        55,
        1,
        55,
        2,
        53,
        55,
        53,
        4,
        53,
        1001,
        56,
        -1,
        56,
        1005,
        56,
        6,
        99,
        0,
        0,
        0,
        0,
        10,
    ]


class Day07TestCase(TestCase):
    def test_part1(self):
        file_data = parse("../input.txt")
        [max_val, max_seq] = part1(file_data)
        self.assertEqual(max_val, 13848)

    def test_part2(self):
        file_data = parse("../input.txt")
        [max_val, max_seq] = part2(file_data)
        self.assertEqual(max_val, 12932154)

    def test_amplify_once(self):
        test_cases = []
        test_cases.append([Programs7.prog_a_1, [4, 3, 2, 1, 0], 43210])
        test_cases.append([Programs7.prog_a_2, [0, 1, 2, 3, 4], 54321])
        test_cases.append([Programs7.prog_a_3, [1, 0, 4, 3, 2], 65210])
        for test_case in test_cases:
            prog = test_case[0]
            phase_setting = test_case[1]
            want_val = test_case[2]
            got_val = amplify_once(prog, phase_setting)
            self.assertEqual(want_val, got_val)

    def test_amplify_once_find_max_seq(self):
        test_cases = []
        test_cases.append([Programs7.prog_a_1, [4, 3, 2, 1, 0], 43210])
        test_cases.append([Programs7.prog_a_2, [0, 1, 2, 3, 4], 54321])
        test_cases.append([Programs7.prog_a_3, [1, 0, 4, 3, 2], 65210])
        for test_case in test_cases:
            prog = test_case[0]
            want_seq = test_case[1]
            want_val = test_case[2]
            [got_val, got_seq] = amplify_once_find_max_seq(prog)
            self.assertEqual(want_val, got_val)
            self.assertEqual(want_seq, got_seq)

    def test_amplify_loop(self):
        test_cases = []
        test_cases.append([Programs7.prog_b_1, [9, 8, 7, 6, 5], 139629729])
        test_cases.append([Programs7.prog_b_2, [9, 7, 8, 5, 6], 18216])
        for test_case in test_cases:
            prog = test_case[0]
            phase_setting = test_case[1]
            want_val = test_case[2]
            got_val = amplify_loop(prog, phase_setting)
            self.assertEqual(want_val, got_val)

    def test_amplify_loop_max_seq(self):
        test_cases = []
        test_cases.append([Programs7.prog_b_1, [9, 8, 7, 6, 5], 139629729])
        test_cases.append([Programs7.prog_b_2, [9, 7, 8, 5, 6], 18216])
        for test_case in test_cases:
            prog = test_case[0]
            want_seq = test_case[1]
            want_val = test_case[2]
            [got_val, got_seq] = amplify_loop_max_seq(prog)
            self.assertEqual(want_val, got_val)
            self.assertEqual(want_seq, got_seq)


if __name__ == "__main__":
    main()
