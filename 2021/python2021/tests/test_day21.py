#!/usr/bin/env python3
"""
Test Day21.
"""

import unittest
from aoc.day21 import Day21


class TestDay21(unittest.TestCase):
    """Test Day21."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day21.part1("../inputs/21/input.txt"), 1073709)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day21.part2("../inputs/21/input.txt"), 148747830493442)


if __name__ == "__main__":
    unittest.main()
