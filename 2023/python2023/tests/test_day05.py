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
        self.assertEqual(Day05.part1("../inputs/05/input_small.txt"), 35)
        self.assertEqual(Day05.part1("../inputs/05/input.txt"), 227653707)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day05.part2("../inputs/05/input_small.txt"), 46)
        ##self.assertEqual(Day05.part2("../inputs/05/input.txt"), 10378710)


if __name__ == "__main__":
    unittest.main()
