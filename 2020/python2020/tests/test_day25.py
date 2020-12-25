#!/usr/bin/env python3
"""
Test Day25.
"""

import unittest
from aoc.day25 import p1


class TestDay25(unittest.TestCase):
    """Test Day25."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(p1([5764801, 17807724]), 14897079)
        self.assertEqual(p1([2069194, 16426071]), 11576351)


if __name__ == "__main__":
    unittest.main()
