#!/usr/bin/env python3

"""
Test Day03.
"""

import unittest
from day03 import Day03


class TestBasic(unittest.TestCase):
    """Test Day03."""

    def test_part1(self):
        """Test part1"""
        cases = [[1, 0], [12, 3], [23, 2], [1024, 31]]
        for case in cases:
            got = Day03.part1(case[0])
            want = case[1]
            self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
