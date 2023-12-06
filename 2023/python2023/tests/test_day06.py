#!/usr/bin/env python3
"""
Test Day06.
"""

import unittest
from aoc.day06 import Day06


class TestDay06(unittest.TestCase):
    """Test Day06."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day06.part1("../inputs/06/input_small.txt"), 288)
        self.assertEqual(Day06.part1("../inputs/06/input.txt"), 4568778)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day06.part2("../inputs/06/input_small.txt"), 71503)
        self.assertEqual(Day06.part2("../inputs/06/input.txt"), 28973936)


if __name__ == "__main__":
    unittest.main()
