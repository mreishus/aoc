#!/usr/bin/env python3
"""
Test Day19.
"""

import unittest
from aoc.day19 import Day19


class TestDay19(unittest.TestCase):
    """Test Day19."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day19.part1("../inputs/19/input.txt"), 338)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day19.part2("../inputs/19/input.txt"), 9862)


if __name__ == "__main__":
    unittest.main()
