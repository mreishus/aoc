#!/usr/bin/env python3
"""
Test Day15.
"""

import unittest
from aoc.day15 import Day15, helper


class TestDay15(unittest.TestCase):
    """Test Day15."""

    def test_p1_examples(self):
        def p1(array):
            return helper(array, 2020)

        self.assertEqual(p1([1, 3, 2]), 1)
        self.assertEqual(p1([2, 1, 3]), 10)
        self.assertEqual(p1([1, 2, 3]), 27)
        self.assertEqual(p1([2, 3, 1]), 78)
        self.assertEqual(p1([3, 2, 1]), 438)
        self.assertEqual(p1([3, 1, 2]), 1836)

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day15.part1("../inputs/15/input.txt"), 496)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day15.part2("../inputs/15/input.txt"), 883)


if __name__ == "__main__":
    unittest.main()
