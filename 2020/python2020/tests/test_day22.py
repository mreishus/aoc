#!/usr/bin/env python3
"""
Test Day22.
"""

import unittest
from aoc.day22 import Day22


class TestDay22(unittest.TestCase):
    """Test Day22."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day22.part1("../inputs/22/input_small_1.txt"), 306)
        self.assertEqual(Day22.part1("../inputs/22/input.txt"), 35370)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day22.part2("../inputs/22/input_small_1.txt"), 291)
        self.assertEqual(Day22.part2("../inputs/22/input.txt"), 36246)


if __name__ == "__main__":
    unittest.main()
