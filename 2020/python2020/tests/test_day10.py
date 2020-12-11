#!/usr/bin/env python3
"""
Test Day10.
"""

import unittest
from aoc.day10 import Day10


class TestDay10(unittest.TestCase):
    """Test Day10."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day10.part1("../inputs/10/input_small_1.txt"), 35)
        self.assertEqual(Day10.part1("../inputs/10/input_small_2.txt"), 220)
        self.assertEqual(Day10.part1("../inputs/10/input.txt"), 2312)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day10.part2("../inputs/10/input_small_1.txt"), 8)
        self.assertEqual(Day10.part2("../inputs/10/input_small_2.txt"), 19208)
        self.assertEqual(Day10.part2("../inputs/10/input.txt"), 12089663946752)


if __name__ == "__main__":
    unittest.main()
