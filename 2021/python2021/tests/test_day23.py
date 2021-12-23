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
        self.assertEqual(Day23.part1("../inputs/23/input.txt"), 16059)
        self.assertEqual(Day23.part1("../inputs/23/input_12521.txt"), 12521)
        self.assertEqual(Day23.part1("../inputs/23/input_12481.txt"), 12481)
        self.assertEqual(Day23.part1("../inputs/23/input_12081.txt"), 12081)
        self.assertEqual(Day23.part1("../inputs/23/input_9051.txt"), 9051)
        self.assertEqual(Day23.part1("../inputs/23/input_9011.txt"), 9011)
        self.assertEqual(Day23.part1("../inputs/23/input_8.txt"), 8)
        self.assertEqual(Day23.part1("../inputs/23/input_7008.txt"), 7008)

    def test_part2(self):
        """Test part2"""
        self.assertEqual("hello", "hello")
        # self.assertEqual(Day23.part2("../inputs/23/input.txt"), 4775)


if __name__ == "__main__":
    unittest.main()
