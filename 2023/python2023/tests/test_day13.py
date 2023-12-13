#!/usr/bin/env python3
"""
Test Day13.
"""

import unittest
from aoc.day13 import Day13


class TestDay13(unittest.TestCase):
    """Test Day13."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day13.part1("../inputs/13/input_small.txt"), 405)
        self.assertEqual(Day13.part1("../inputs/13/input.txt"), 34993)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day13.part2("../inputs/13/input_small.txt"), 400)
        self.assertEqual(Day13.part2("../inputs/13/input.txt"), 29341)


if __name__ == "__main__":
    unittest.main()
