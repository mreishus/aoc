#!/usr/bin/env python3
"""
Test Day12.
"""

import unittest
from aoc.day12 import Day12, is_valid, is_valid_definite_prefix


class TestDay12(unittest.TestCase):
    """Test Day12."""

    def test_valid_cases(self):
        self.assertTrue(is_valid("...###...##..", [3, 2]))
        self.assertTrue(is_valid("####...##.", [4, 2]))
        self.assertTrue(is_valid("#..###.#", [1, 3, 1]))
        self.assertTrue(is_valid("....", []))
        self.assertTrue(is_valid("#", [1]))

    def test_invalid_cases(self):
        self.assertFalse(is_valid("...###...##..", [3, 3]))
        self.assertFalse(is_valid("####...##.", [5, 2]))
        self.assertFalse(is_valid("#..###.#", [1, 3, 2]))
        self.assertFalse(is_valid("....", [1]))
        self.assertFalse(is_valid("#", []))

    def test_potentially_valid_cases(self):
        self.assertTrue(is_valid_definite_prefix("...###?..##..", [3]))
        self.assertTrue(is_valid_definite_prefix("####...?##.", [4]))
        self.assertTrue(is_valid_definite_prefix("#..###?#", [1, 3]))
        self.assertTrue(is_valid_definite_prefix("....?", []))
        self.assertTrue(is_valid_definite_prefix("#?", [1]))

    def test_potentially_invalid_cases(self):
        self.assertFalse(is_valid_definite_prefix("...###?..##..", [2]))
        self.assertFalse(is_valid_definite_prefix("####...?##.", [5]))
        # self.assertFalse(is_valid_definite_prefix("#..###?#", [1, 4])) Not smart enough to detect this

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day12.part1("../inputs/12/input_small.txt"), 21)
        self.assertEqual(Day12.part1("../inputs/12/input.txt"), 8193)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day12.part2("../inputs/12/input_small.txt"), 525152)
        self.assertEqual(Day12.part2("../inputs/12/input.txt"), 45322533163795)


if __name__ == "__main__":
    unittest.main()
