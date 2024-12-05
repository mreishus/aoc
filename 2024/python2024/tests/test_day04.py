#!/usr/bin/env python3
"""
Test Day04.
"""

import unittest
from aoc.day04 import Day04


class TestDay04(unittest.TestCase):
    """Test Day04."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day04.part1("../inputs/04/input_small.txt"), 18)
        self.assertEqual(Day04.part1("../inputs/04/input.txt"), 2583)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day04.part2("../inputs/04/input_small.txt"), 9)
        self.assertEqual(Day04.part2("../inputs/04/input.txt"), 1978)


if __name__ == "__main__":
    unittest.main()
