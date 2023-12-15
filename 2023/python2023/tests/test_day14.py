#!/usr/bin/env python3
"""
Test Day14.
"""

import unittest
from aoc.day14 import Day14


class TestDay14(unittest.TestCase):
    """Test Day14."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day14.part1("../inputs/14/input_small.txt"), 136)
        self.assertEqual(Day14.part1("../inputs/14/input.txt"), 108826)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day14.part2("../inputs/14/input_small.txt"), 64)
        self.assertEqual(Day14.part2("../inputs/14/input.txt"), 99291)


if __name__ == "__main__":
    unittest.main()
