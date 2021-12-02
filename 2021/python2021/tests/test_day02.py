#!/usr/bin/env python3
"""
Test Day02.
"""

import unittest
from aoc.day02 import Day02


class TestDay02(unittest.TestCase):
    """Test Day02."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day02.part1("../inputs/02/input_small.txt"), -1)
        # self.assertEqual(Day02.part1("../inputs/02/input.txt"), 1298)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day02.part2("../inputs/02/input_small.txt"), -1)
        # self.assertEqual(Day02.part2("../inputs/02/input.txt"), 1248)


if __name__ == "__main__":
    unittest.main()
