#!/usr/bin/env python
from unittest import TestCase, main

from day19 import parse
from aoc.day19 import Day19
from aoc.day17 import Day17Droid
from aoc.day15 import Day15
from aoc.breakout import Breakout
from aoc.painter_robot import PainterRobot
from aoc.computer import solve1
from aoc.amplify import (
    amplify_once,
    amplify_once_find_max_seq,
    amplify_loop,
    amplify_loop_max_seq,
)


class Programs5:
    prog_larger = [
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


class Day19TestCase(TestCase):
    def test_part1(self):
        program = parse("../../19/input.txt")
        d9 = Day19(program)
        got = d9.part1()
        want = 141
        self.assertEqual(got, want)

    def test_part2(self):
        print(
            "Day 19 Part 2: This test is slow, comment out for a faster feedback loop"
        )
        program = parse("../../19/input.txt")
        d9 = Day19(program)
        got = d9.part2()
        want = 15641348
        self.assertEqual(got, want)


class Day17TestCase(TestCase):
    def test_part1(self):
        program = parse("../../17/input.txt")
        droid = Day17Droid(program)
        got = droid.part1()
        want = 13580
        self.assertEqual(want, got)

    def test_part2(self):
        program = parse("../../17/input.txt")
        droid = Day17Droid(program)
        got = droid.part2()
        want = 1063081
        self.assertEqual(want, got)


class Day15TestCase(TestCase):
    def test_part1_and2(self):
        program = parse("../../15/input.txt")
        p1, p2 = Day15.part1_and_2(program)
        self.assertEqual(p1, 226)
        self.assertEqual(p2, 342)


class Day13TestCase(TestCase):
    def test_part1(self):
        program = parse("../../13/input.txt")
        got = Breakout.part1(program)
        self.assertEqual(got, 270)

    def test_part2(self):
        program = parse("../../13/input.txt")
        got = Breakout.part1(program)
        self.assertEqual(got, 270)


class Day11TestCase(TestCase):
    def test_part1(self):
        program = parse("../../11/input.txt")
        got = PainterRobot.part1(program)
        self.assertEqual(got, 2539)

    def test_part2(self):
        program = parse("../../11/input.txt")
        got = PainterRobot.part1(program, initial_color=1)
        self.assertEqual(got, 249)


class Day09TestCase(TestCase):
    def test_prog1(self):
        test_prog1 = [
            109,
            1,
            204,
            -1,
            1001,
            100,
            1,
            100,
            1008,
            100,
            16,
            101,
            1006,
            101,
            0,
            99,
        ]
        outputs = solve1(test_prog1, [])
        # Quine
        self.assertEqual(outputs, test_prog1)

    def test_prog2(self):
        test_prog2 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
        outputs = solve1(test_prog2, [])
        self.assertEqual(outputs, [1219070632396864])

    def test_prog3(self):
        test_prog3 = [104, 1125899906842624, 99]
        outputs = solve1(test_prog3, [])
        self.assertEqual(outputs, [1125899906842624])

    def test_part1(self):
        file_data = parse("../../09/input.txt")
        outputs = solve1(file_data, [1])
        self.assertEqual(outputs, [3780860499])

    def test_part2(self):
        file_data = parse("../../09/input.txt")
        outputs = solve1(file_data, [2])
        self.assertEqual(outputs, [33343])


class Day07TestCase(TestCase):
    def test_part1(self):
        file_data = parse("../../07/input.txt")
        [max_val, max_seq] = amplify_once_find_max_seq(file_data)
        self.assertEqual(max_val, 13848)

    def test_part2(self):
        file_data = parse("../../07/input.txt")
        [max_val, max_seq] = amplify_loop_max_seq(file_data)
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

    def test_8_1(self):
        program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        self.assertEqual(solve1(program, [7]), [0])
        self.assertEqual(solve1(program, [8]), [1])
        self.assertEqual(solve1(program, [9]), [0])

    def test_8_2(self):
        program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        self.assertEqual(solve1(program, [7]), [1])
        self.assertEqual(solve1(program, [8]), [0])
        self.assertEqual(solve1(program, [9]), [0])

    def test_8_3(self):
        program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        self.assertEqual(solve1(program, [7]), [0])
        self.assertEqual(solve1(program, [8]), [1])
        self.assertEqual(solve1(program, [9]), [0])

    def test_8_4(self):
        program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        self.assertEqual(solve1(program, [7]), [1])
        self.assertEqual(solve1(program, [8]), [0])
        self.assertEqual(solve1(program, [9]), [0])

    def test_jump_1(self):
        program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
        self.assertEqual(solve1(program, [0]), [0])
        self.assertEqual(solve1(program, [10]), [1])

    def test_jump_2(self):
        program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
        self.assertEqual(solve1(program, [0]), [0])
        self.assertEqual(solve1(program, [10]), [1])

    def test_larger(self):
        program = Programs5.prog_larger
        self.assertEqual(solve1(program, [2]), [999])
        self.assertEqual(solve1(program, [8]), [1000])
        self.assertEqual(solve1(program, [12]), [1001])

    def test_day5_part1(self):
        file_data = parse("../../05/input.txt")
        got = solve1(file_data, [1])
        want = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5821753]
        self.assertEqual(want, got)

    def test_day5_part2(self):
        file_data = parse("../../05/input.txt")
        got = solve1(file_data, [5])
        want = [11956381]
        self.assertEqual(want, got)


if __name__ == "__main__":
    main()
