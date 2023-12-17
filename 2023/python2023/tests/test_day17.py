#!/usr/bin/env python3
"""
Test Day17.
"""

import unittest
from aoc.day17 import Day17


class TestDay17(unittest.TestCase):
    """Test Day17."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day17.part1("../inputs/17/input_small.txt"), 102)
        self.assertEqual(Day17.part1("../inputs/17/input.txt"), 694)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day17.part2("../inputs/17/input_small.txt"), 94)
        self.assertEqual(Day17.part2("../inputs/17/input_small2.txt"), 71)
        self.assertEqual(Day17.part2("../inputs/17/input.txt"), 829)


if __name__ == "__main__":
    unittest.main()
