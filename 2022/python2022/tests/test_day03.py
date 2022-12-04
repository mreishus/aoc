#!/usr/bin/env python3
"""
Test Day03.
"""

import unittest
from aoc.day03 import Day03


class TestDay03(unittest.TestCase):
    """Test Day03."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day03.part1("../inputs/03/input_small.txt"), 157)
        self.assertEqual(Day03.part1("../inputs/03/input.txt"), 8072)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day03.part2("../inputs/03/input_small.txt"), 70)
        self.assertEqual(Day03.part2("../inputs/03/input.txt"), 2567)


if __name__ == "__main__":
    unittest.main()
