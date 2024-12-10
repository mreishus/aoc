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
        self.assertEqual(Day10.part1("../inputs/10/input_small2.txt"), 36)
        self.assertEqual(Day10.part1("../inputs/10/input.txt"), 786)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day10.part2("../inputs/10/input_small2.txt"), 81)
        self.assertEqual(Day10.part2("../inputs/10/input.txt"), 1722)
        


if __name__ == "__main__":
    unittest.main()
