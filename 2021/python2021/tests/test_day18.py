#!/usr/bin/env python3
"""
Test Day18.
"""

import unittest
from aoc.day18 import Day18


class TestDay18(unittest.TestCase):
    """Test Day18."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day18.part1("../inputs/18/input.txt"), 3665)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day18.part2("../inputs/18/input.txt"), 4775)


if __name__ == "__main__":
    unittest.main()
