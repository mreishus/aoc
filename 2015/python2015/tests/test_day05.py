#!/usr/bin/env python3
"""
Test Day05.
"""

import unittest
from aoc.day05 import Day05, is_nice1, is_nice2


class TestDay05(unittest.TestCase):
    """Test Day05."""

    def test_is_nice1(self):
        """Test is_nice1"""
        self.assertEqual(is_nice1("ugknbfddgicrmopn"), True)
        self.assertEqual(is_nice1("bbb"), False)
        self.assertEqual(is_nice1("aaa"), True)
        self.assertEqual(is_nice1("jchzalrnumimnmhp"), False)
        self.assertEqual(is_nice1("haegwjzuvuyypxyu"), False)
        self.assertEqual(is_nice1("dvszwmarrgswjxmb"), False)

    def test_is_nice2(self):
        """Test is_nice2"""
        self.assertEqual(is_nice2("qjhvhtzxzqqjkmpb"), True)
        self.assertEqual(is_nice2("xxyxx"), True)
        self.assertEqual(is_nice2("uurcxstgmygtbstg"), False)
        self.assertEqual(is_nice2("ieodomkazucvgmuy"), False)


if __name__ == "__main__":
    unittest.main()
