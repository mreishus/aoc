#!/usr/bin/env python
"""
Test Day11.
"""

import unittest
from aoc.day11 import inc, is_valid, next_pw


class TestDay11(unittest.TestCase):
    """Test Day11."""

    def test_inc(self):
        pws = ["xx", "xy", "xz", "ya", "yb"]
        for (pw1, pw2) in zip(pws, pws[1:]):
            self.assertEqual(inc(pw1), pw2)

    def test_is_valid(self):
        self.assertEqual(is_valid("hijklmmn"), False)
        self.assertEqual(is_valid("abbceffg"), False)
        self.assertEqual(is_valid("abbcegjk"), False)
        self.assertEqual(is_valid("abcdffaa"), True)
        self.assertEqual(is_valid("ghjaabcc"), True)

    def test_next_pw(self):
        self.assertEqual(next_pw("abcdefgh"), "abcdffaa")
        self.assertEqual(next_pw("ghijklmn"), "ghjaabcc")
