#!/usr/bin/env python3
"""
Test Day01.
"""

import unittest
from aoc.day01 import Day01


class TestDay01(unittest.TestCase):
    """Test Day01."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day01.part1("../inputs/01/input_small.txt"), 142)
        self.assertEqual(Day01.part1("../inputs/01/input.txt"), 54601)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day01.part2("../inputs/01/input_small2.txt"), 281)
        self.assertEqual(Day01.part2("../inputs/01/input.txt"), 54078)


if __name__ == "__main__":
    unittest.main()
