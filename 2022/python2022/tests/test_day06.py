#!/usr/bin/env python3
"""
Test Day06.
"""

import unittest
from aoc.day06 import Day06


class TestDay06(unittest.TestCase):
    """Test Day06."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day06.part1("../inputs/06/input_small.txt"), 7)
        self.assertEqual(Day06.part1("../inputs/06/input_small2.txt"), 5)
        self.assertEqual(Day06.part1("../inputs/06/input_small3.txt"), 6)
        self.assertEqual(Day06.part1("../inputs/06/input_small4.txt"), 10)
        self.assertEqual(Day06.part1("../inputs/06/input.txt"), 1655)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day06.part2("../inputs/06/input_small.txt"), 19)
        self.assertEqual(Day06.part2("../inputs/06/input_small2.txt"), 23)
        self.assertEqual(Day06.part2("../inputs/06/input_small3.txt"), 23)
        self.assertEqual(Day06.part2("../inputs/06/input_small4.txt"), 29)
        self.assertEqual(Day06.part2("../inputs/06/input.txt"), 2665)


if __name__ == "__main__":
    unittest.main()
