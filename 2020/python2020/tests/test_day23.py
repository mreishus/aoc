#!/usr/bin/env python3
"""
Test Day23.
"""

import unittest
from aoc.day23 import Day23


class TestDay23(unittest.TestCase):
    """Test Day23."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day23.part1("../inputs/23/input_small_1.txt"), "67384529")
        self.assertEqual(Day23.part1("../inputs/23/input.txt"), "82934675")

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day23.part2("../inputs/23/input_small_1.txt"), 149245887792)
        self.assertEqual(Day23.part2("../inputs/23/input.txt"), 474600314018)


if __name__ == "__main__":
    unittest.main()
