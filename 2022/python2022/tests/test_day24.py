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
        self.assertEqual(Day24.part1("../inputs/24/input_small2.txt"), 18)
        self.assertEqual(Day24.part1("../inputs/24/input.txt"), 232)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day24.part2("../inputs/24/input_small2.txt"), 54)
        self.assertEqual(Day24.part2("../inputs/24/input.txt"), 715)


if __name__ == "__main__":
    unittest.main()
