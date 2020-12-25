#!/usr/bin/env python3
"""
Test Day16.
"""

import unittest
from aoc.day16 import Day16


class TestDay16(unittest.TestCase):
    """Test Day16."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day16.part1("../inputs/16/input_small_1.txt"), 71)
        self.assertEqual(Day16.part1("../inputs/16/input.txt"), 26988)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day16.part2("../inputs/16/input_small_1.txt"), 1)
        self.assertEqual(Day16.part2("../inputs/16/input.txt"), 426362917709)


if __name__ == "__main__":
    unittest.main()
