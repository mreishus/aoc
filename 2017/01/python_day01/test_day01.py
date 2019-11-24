#!/usr/bin/env python3
"""
Test Day01.
"""

import unittest
from day01 import Day01


class TestBasic(unittest.TestCase):
    """Test Day01."""

    def test_rotate(self):
        """Test rotate"""
        self.assertEqual(Day01.rotate("abcd", 1), "bcda")
        self.assertEqual(Day01.rotate("1234", 1), "2341")
        self.assertEqual(Day01.rotate("1234", 2), "3412")

    def test_part1(self):
        """Test part1"""
        cases = [["1122", 3], ["1111", 4], ["1234", 0], ["91212129", 9]]
        for case in cases:
            input_str, want = case
            got = Day01.part1(input_str)
            self.assertEqual(want, got)

    def test_part2(self):
        """Test part2"""
        cases = [
            ["1212", 6],
            ["1221", 0],
            ["123425", 4],
            ["123123", 12],
            ["12131415", 4],
        ]
        for case in cases:
            input_str, want = case
            got = Day01.part2(input_str)
            self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
