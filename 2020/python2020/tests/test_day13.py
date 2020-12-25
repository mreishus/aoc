#!/usr/bin/env python3
"""
Test Day13.
"""

import unittest
from aoc.day13 import Day13, p1, p2


class TestDay13(unittest.TestCase):
    """Test Day13."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day13.part1("../inputs/13/input_small_1.txt"), 295)
        self.assertEqual(Day13.part1("../inputs/13/input.txt"), 3966)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day13.part2("../inputs/13/input_small_1.txt"), 1068781)
        self.assertEqual(Day13.part2("../inputs/13/input.txt"), 800177252346225)


if __name__ == "__main__":
    unittest.main()
