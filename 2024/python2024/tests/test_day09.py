#!/usr/bin/env python3
"""
Test Day09.
"""

import unittest
from aoc.day09 import Day09


class TestDay09(unittest.TestCase):
    """Test Day09."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day09.part1("../inputs/09/input_small.txt"), 1928)
        self.assertEqual(Day09.part1("../inputs/09/input.txt"), 6359213660505)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day09.part2("../inputs/09/input_small.txt"), 2858)
        self.assertEqual(Day09.part2("../inputs/09/input.txt"), 6381624803796)
        


if __name__ == "__main__":
    unittest.main()
