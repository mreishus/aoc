#!/usr/bin/env python3
"""
Test Day08.
"""

import unittest
from aoc.day08 import Day08


class TestDay08(unittest.TestCase):
    """Test Day08."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day08.part1("../inputs/08/input_small2.txt"), 26)
        self.assertEqual(Day08.part1("../inputs/08/input.txt"), 514)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day08.part2("../inputs/08/input_small2.txt"), 61229)
        self.assertEqual(Day08.part2("../inputs/08/input.txt"), 1012272)


if __name__ == "__main__":
    unittest.main()
