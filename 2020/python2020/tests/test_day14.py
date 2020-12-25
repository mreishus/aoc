#!/usr/bin/env python3
"""
Test Day14.
"""

import unittest
from aoc.day14 import Day14, Mask


class TestDay14(unittest.TestCase):
    """Test Day14."""

    def test_empty_mask(self):
        m = Mask()
        for i in range(1, 5000):
            j = m.apply_over_value(i)
            self.assertEqual(i, j)

    def test_mask_example(self):
        m = Mask()
        m.update_from_string("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
        self.assertEqual(m.apply_over_value(11), 73)
        self.assertEqual(m.apply_over_value(101), 101)
        self.assertEqual(m.apply_over_value(0), 64)

    def test_mask_0_then_1(self):
        m = Mask()
        m.update_from_string("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX0X")
        self.assertEqual(m.apply_over_value(3), 1)
        self.assertEqual(m.apply_over_value(1), 1)
        m.update_from_string("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX1X")
        self.assertEqual(m.apply_over_value(3), 3)
        self.assertEqual(m.apply_over_value(1), 3)

    def test_mask_1_then_0(self):
        m = Mask()
        m.update_from_string("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX1X")
        self.assertEqual(m.apply_over_value(3), 3)
        self.assertEqual(m.apply_over_value(1), 3)
        m.update_from_string("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX0X")
        self.assertEqual(m.apply_over_value(3), 1)
        self.assertEqual(m.apply_over_value(1), 1)

    def test_complicated_mask(self):
        m = Mask()
        m.update_from_string("010X1100101X00X01001X11010X111100X01")
        # Mask = 010X1100101X00X01001X11010X111100X01
        #    0 = 000000000000000000000000000000000000
        #  out = 010011001010000010010110100111100001
        self.assertEqual(m.apply_over_value(0), 20569483745)

    def test_part1(self):
        """Test part1"""
        self.assertEqual(Day14.part1("../inputs/14/input_small_1.txt"), 165)
        self.assertEqual(Day14.part1("../inputs/14/input.txt"), 15514035145260)

    def test_part2(self):
        """Test part2"""
        self.assertEqual(Day14.part2("../inputs/14/input_small_2.txt"), 208)
        self.assertEqual(Day14.part2("../inputs/14/input.txt"), 3926790061594)


if __name__ == "__main__":
    unittest.main()
