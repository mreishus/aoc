#!/usr/bin/env python3
"""
Test Day12.
"""

import unittest
from aoc.day12 import Day12


class TestDay12(unittest.TestCase):
    """Test Day12."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day12.part1("../inputs/12/input_small.txt"), 31)
        self.assertEqual(Day12.part1("../inputs/12/input.txt"), 425)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day12.part2("../inputs/12/input_small.txt"), 29)
        self.assertEqual(Day12.part2("../inputs/12/input.txt"), 418)


if __name__ == "__main__":
    unittest.main()
