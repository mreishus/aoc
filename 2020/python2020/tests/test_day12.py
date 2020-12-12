#!/usr/bin/env python3
"""
Test Day12.
"""

import unittest
from aoc.day12 import Day12, p1, p2


class TestDay12(unittest.TestCase):
    """Test Day12."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day12.part1("../inputs/12/input_small_1.txt"), 25)
        self.assertEqual(Day12.part1("../inputs/12/input.txt"), 562)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day12.part2("../inputs/12/input_small_1.txt"), 286)
        self.assertEqual(Day12.part2("../inputs/12/input.txt"), 101860)


if __name__ == "__main__":
    unittest.main()
