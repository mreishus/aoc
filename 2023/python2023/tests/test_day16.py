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
        self.assertEqual(Day16.part1("../inputs/16/input_small.txt"), 46)
        self.assertEqual(Day16.part1("../inputs/16/input.txt"), 7415)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day16.part2("../inputs/16/input_small.txt"), 51)
        self.assertEqual(Day16.part2("../inputs/16/input.txt"), 7943)


if __name__ == "__main__":
    unittest.main()
