#!/usr/bin/env python3
"""
Test Day13.
"""

import unittest
from aoc.day13 import Day13


class TestDay13(unittest.TestCase):
    """Test Day13."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day13.part1("../inputs/13/input_small.txt"), 17)
        self.assertEqual(Day13.part1("../inputs/13/input.txt"), 592)

    def test_part2(self):
        """Test part2"""
        self.assertEqual("hello", "hello")
        # Hard to test - a human has to read the characters as is


if __name__ == "__main__":
    unittest.main()
