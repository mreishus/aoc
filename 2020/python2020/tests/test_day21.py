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
        self.assertEqual(Day21.part1("../inputs/21/input_small_1.txt"), 5)
        self.assertEqual(Day21.part1("../inputs/21/input.txt"), 2826)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(
            Day21.part2("../inputs/21/input_small_1.txt"), "mxmxvkd,sqjhc,fvjkl"
        )
        self.assertEqual(
            Day21.part2("../inputs/21/input.txt"),
            "pbhthx,sqdsxhb,dgvqv,csnfnl,dnlsjr,xzb,lkdg,rsvlb",
        )


if __name__ == "__main__":
    unittest.main()
