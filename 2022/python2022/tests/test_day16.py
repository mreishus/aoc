#!/usr/bin/env python3
"""
Test Day16.
"""

import unittest
from aoc.day16 import Day16


class TestDay16(unittest.TestCase):
    """Test Day16."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day16.part1("../inputs/16/input_small.txt"), 1651)
        self.assertEqual(Day16.part1("../inputs/16/input.txt"), 1828)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day16.part2("../inputs/16/input_small.txt"), 1707)
        self.assertEqual(Day16.part2("../inputs/16/input.txt"), 2292)


if __name__ == "__main__":
    unittest.main()
