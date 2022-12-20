#!/usr/bin/env python3
"""
Test Day10.
"""

import unittest
from aoc.day10 import Day10


class TestDay10(unittest.TestCase):
    """Test Day10."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day10.part1("../inputs/10/input_small2.txt"), 13140)
        self.assertEqual(Day10.part1("../inputs/10/input.txt"), 12520)


if __name__ == "__main__":
    unittest.main()
