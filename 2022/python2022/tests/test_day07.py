#!/usr/bin/env python3
"""
Test Day07.
"""

import unittest
from aoc.day07 import Day07


class TestDay07(unittest.TestCase):
    """Test Day07."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day07.part1("../inputs/07/input_small.txt"), 95437)
        self.assertEqual(Day07.part1("../inputs/07/input.txt"), 1428881)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day07.part2("../inputs/07/input_small.txt"), 24933642)
        self.assertEqual(Day07.part2("../inputs/07/input.txt"), 10475598)


if __name__ == "__main__":
    unittest.main()
