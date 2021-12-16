#!/usr/bin/env python3
"""
Test Day16.
"""

import unittest
from aoc.day16 import Day16


class TestDay16(unittest.TestCase):
    """Test Day16."""

    def test_part1(self):
        """Test part1"""
        self.assertEqual("hello", "hello")
        # self.assertEqual(Day16.part1("../inputs/16/input_small.txt"), 1588)
        # self.assertEqual(Day16.part1("../inputs/16/input.txt"), 3058)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day16.part2_hexstring("C200B40A82"), 3)
        self.assertEqual(Day16.part2_hexstring("04005AC33890"), 54)
        self.assertEqual(Day16.part2_hexstring("880086C3E88112"), 7)
        self.assertEqual(Day16.part2_hexstring("CE00C43D881120"), 9)
        self.assertEqual(Day16.part2_hexstring("D8005AC2A8F0"), 1)
        self.assertEqual(Day16.part2_hexstring("F600BC2D8F"), 0)
        self.assertEqual(Day16.part2_hexstring("9C005AC2F8F0"), 0)
        self.assertEqual(Day16.part2_hexstring("9C0141080250320F1802104A08"), 1)
        self.assertEqual(Day16.part2("../inputs/16/input.txt"), 911945136934)


if __name__ == "__main__":
    unittest.main()
