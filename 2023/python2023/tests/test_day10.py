#!/usr/bin/env python3
"""
Test Day10.
"""

import unittest
from aoc.day10 import Day10


class TestDay10(unittest.TestCase):
    """Test Day10."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day10.part1("../inputs/10/input_small.txt"), 4)
        self.assertEqual(Day10.part1("../inputs/10/input_small2.txt"), 4)
        self.assertEqual(Day10.part1("../inputs/10/input_small3.txt"), 8)
        self.assertEqual(Day10.part1("../inputs/10/input_small4.txt"), 8)
        self.assertEqual(Day10.part1("../inputs/10/input.txt"), 6897)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day10.part2("../inputs/10/input_small5.txt"), 4)
        self.assertEqual(Day10.part2("../inputs/10/input_small6.txt"), 4)
        self.assertEqual(Day10.part2("../inputs/10/input_small7.txt"), 8)
        self.assertEqual(Day10.part2("../inputs/10/input_small8.txt"), 10)
        self.assertEqual(Day10.part2("../inputs/10/input.txt"), 367)


if __name__ == "__main__":
    unittest.main()
