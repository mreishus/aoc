#!/usr/bin/env python3
"""
Test Day10.
"""

import unittest
from aoc.day10 import expand


class TestDay10(unittest.TestCase):
    """Test Day10."""

    def test_expand(self):
        self.assertEqual(expand("1"), "11")
        self.assertEqual(expand("11"), "21")
        self.assertEqual(expand("21"), "1211")
        self.assertEqual(expand("1211"), "111221")
        self.assertEqual(expand("111221"), "312211")
