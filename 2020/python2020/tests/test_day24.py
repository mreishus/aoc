#!/usr/bin/env python3
"""
Test Day24.
"""

import unittest
from aoc.day24 import Day24


class TestDay24(unittest.TestCase):
    """Test Day24."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day24.part1("../inputs/24/input_small_1.txt"), 10)
        self.assertEqual(Day24.part1("../inputs/24/input.txt"), 497)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day24.part2("../inputs/24/input_small_1.txt"), 2208)
        self.assertEqual(Day24.part2("../inputs/24/input.txt"), 4156)


if __name__ == "__main__":
    unittest.main()
