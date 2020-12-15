#!/usr/bin/env python3
"""
Test Day15.
"""

import unittest
from aoc.day15 import Day15, p1


class TestDay15(unittest.TestCase):
    """Test Day15."""

    def test_p1_examples(self):
        self.assertEqual(p1([1, 3, 2]), 1)
        self.assertEqual(p1([2, 1, 3]), 10)
        self.assertEqual(p1([1, 2, 3]), 27)
        self.assertEqual(p1([2, 3, 1]), 78)
        self.assertEqual(p1([3, 2, 1]), 438)
        self.assertEqual(p1([3, 1, 2]), 1836)

    def test_part1(self):
        """Test part1"""
        pass

    def test_part2(self):
        """Test part2"""
        pass


if __name__ == "__main__":
    unittest.main()
