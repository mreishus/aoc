#!/usr/bin/env python3
"""
Test Day20.
"""

import unittest
from aoc.day20 import Day20


class TestDay20(unittest.TestCase):
    """Test Day20."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day20.part1("../inputs/20/input_small_1.txt"), 20899048083289)
        self.assertEqual(Day20.part1("../inputs/20/input.txt"), 14986175499719)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day20.part2("../inputs/20/input_small_1.txt"), 273)
        self.assertEqual(Day20.part2("../inputs/20/input.txt"), 2161)


if __name__ == "__main__":
    unittest.main()
