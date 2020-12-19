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
        self.assertEqual(Day18.part1("../inputs/18/input_small_1.txt"), 71)
        self.assertEqual(Day18.part1("../inputs/18/input.txt"), 7293529867931)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day18.part2("../inputs/18/input_small_1.txt"), 231)
        self.assertEqual(Day18.part2("../inputs/18/input.txt"), 60807587180737)


if __name__ == "__main__":
    unittest.main()
