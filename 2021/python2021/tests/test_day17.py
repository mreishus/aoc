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
        self.assertEqual(Day17.part1("../inputs/17/input.txt"), 30628)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day17.part2("../inputs/17/input.txt"), 4433)


if __name__ == "__main__":
    unittest.main()
