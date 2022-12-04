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
        self.assertEqual(Day01.part1("../inputs/01/input_small.txt"), 24000)
        self.assertEqual(Day01.part1("../inputs/01/input.txt"), 69912)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day01.part2("../inputs/01/input_small.txt"), 45000)
        self.assertEqual(Day01.part2("../inputs/01/input.txt"), 208180)


if __name__ == "__main__":
    unittest.main()
