#!/usr/bin/env python3
"""
Test Day25.
"""

import unittest
from aoc.day25 import Day25


class TestDay25(unittest.TestCase):
    """Test Day25."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day25.part1("../inputs/25/input.txt"), 582)


if __name__ == "__main__":
    unittest.main()
