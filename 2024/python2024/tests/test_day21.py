#!/usr/bin/env python3
"""
Test Day21.
"""

import unittest
from aoc.day21 import Day21


class TestDay21(unittest.TestCase):
    """Test Day21."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day21.part1("../inputs/21/input_small.txt"), 126384)
        self.assertEqual(Day21.part1("../inputs/21/input.txt"), 222670)

    def test_n4(self):
        self.assertEqual(Day21.part1or2("../inputs/21/input_small.txt", 4), 757754)
        self.assertEqual(Day21.part1or2("../inputs/21/input.txt", 4), 1338784)

    def test_n5(self):
        self.assertEqual(Day21.part1or2("../inputs/21/input_small.txt", 5), 1881090)
        self.assertEqual(Day21.part1or2("../inputs/21/input.txt", 5), 3301126)

    def test_part2(self):
        """Test part2"""
        pass

if __name__ == "__main__":
    unittest.main()
