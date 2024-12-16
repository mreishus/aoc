#!/usr/bin/env python3
"""
Test Day15.
"""

import unittest
from aoc.day15 import Day15


class TestDay15(unittest.TestCase):
    """Test Day15."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day15.part1("../inputs/15/input.txt"), 1476771)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day15.part2("../inputs/15/input.txt"), 1468005)


if __name__ == "__main__":
    unittest.main()
