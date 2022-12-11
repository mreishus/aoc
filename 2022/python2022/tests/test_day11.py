#!/usr/bin/env python3
"""
Test Day11.
"""

import unittest
from aoc.day11 import Day11


class TestDay11(unittest.TestCase):
    """Test Day11."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day11.part1("../inputs/11/input_small.txt"), 10605)
        self.assertEqual(Day11.part1("../inputs/11/input.txt"), 119715)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day11.part2("../inputs/11/input_small.txt"), 2713310158)
        self.assertEqual(Day11.part2("../inputs/11/input.txt"), 18085004878)


if __name__ == "__main__":
    unittest.main()
