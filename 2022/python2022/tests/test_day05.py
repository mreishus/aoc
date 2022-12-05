#!/usr/bin/env python3
"""
Test Day05.
"""

import unittest
from aoc.day05 import Day05


class TestDay05(unittest.TestCase):
    """Test Day05."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day05.part1("../inputs/05/input_small.txt"), "CMZ")
        self.assertEqual(Day05.part1("../inputs/05/input.txt"), "RNZLFZSJH")

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day05.part2("../inputs/05/input_small.txt"), "MCD")
        self.assertEqual(Day05.part2("../inputs/05/input.txt"), "CNSFCGJSM")


if __name__ == "__main__":
    unittest.main()
