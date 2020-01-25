#!/usr/bin/env python3
"""
Test Day08.
"""

import unittest
from aoc.day08 import len_code, len_expand


class TestDay08(unittest.TestCase):
    """Test Day08."""

    def test_len_code(self):
        """Test len_code"""
        str1 = '""'
        self.assertEqual(len(str1), 2)
        self.assertEqual(len_code(str1), 0)

        str2 = '"abc"'
        self.assertEqual(len(str2), 5)
        self.assertEqual(len_code(str2), 3)

        str3 = '"aaa\\"aaa"'
        self.assertEqual(len(str3), 10)
        self.assertEqual(len_code(str3), 7)

        str3 = '"aaa\\"a\\"aa"'
        self.assertEqual(len(str3), 12)
        self.assertEqual(len_code(str3), 8)

        str4 = '"\\x27"'
        self.assertEqual(len(str4), 6)
        self.assertEqual(len_code(str4), 1)

        str5 = '"\\x27jj\\x27"'
        self.assertEqual(len(str5), 12)
        self.assertEqual(len_code(str5), 4)

    def test_len_expand(self):
        """Test len_expand"""
        str1 = '""'
        self.assertEqual(len(str1), 2)
        self.assertEqual(len_expand(str1), 6)

        str2 = '"abc"'
        self.assertEqual(len(str2), 5)
        self.assertEqual(len_expand(str2), 9)

        str3 = '"aaa\\"aaa"'
        self.assertEqual(len(str3), 10)
        self.assertEqual(len_expand(str3), 16)

        str4 = '"\\x27"'
        self.assertEqual(len(str4), 6)
        self.assertEqual(len_expand(str4), 11)

if __name__ == "__main__":
    unittest.main()
