#!/usr/bin/env python3
"""
Test Day14.
"""

import unittest
from aoc.day14 import Day14, p1, p2, Mask


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

    def test_complicated_masks(self):
        m = Mask()
        m.update_from_string("010X1100101X00X01001X11010X111100X01")
        # Mask = 010X1100101X00X01001X11010X111100X01
        #    0 = 000000000000000000000000000000000000
        #  out = 010011001010000010010110100111100001
        self.assertEqual(m.apply_over_value(0), 20569483745)
        m.update_from_string("X101XX001XX1001010X101X1101011100101")

        # Mask1 = 010X1100101X00X01001X11010X111100X01
        # Mask2 = X101XX001XX1001010X101X1101011100101
        # Mask2 = 010111001011001010010111101011100101

        m.update_from_string("X11X110X1011X11X0001011000000X110000")
        # mask = X11X110X1011X11X0001011000000X110000

    # mask = 010X1100101X00X01001X11010X111100X01
    # mem[23014] = 9778
    # mem[42882] = 140716
    # mem[65461] = 458355100
    # mem[60151] = 31172
    # mem[47143] = 7055
    # mask = X101XX001XX1001010X101X1101011100101
    # mem[26134] = 4394
    # mem[18808] = 352500
    # mem[18556] = 87307674
    # mask = X11X110X1011X11X0001011000000X110000

    # 18925954113691
    # 18925954113691

    # Can turn this into a test
    # m = Mask2()
    # m.update_from_string("000000000000000000000000000000X1001X")
    # for z in m.apply_over_value(42):
    #     print(z)
    # print("----")
    # m.update_from_string("00000000000000000000000000000000X0XX")
    # for z in m.apply_over_value(26):
    #     print(z)
    # return -1

    def test_part1(self):
        """Test part1"""
        pass
        # self.assertEqual(Day14.part1("../inputs/14/input_small_1.txt"), 25)
        # self.assertEqual(Day14.part1("../inputs/14/input.txt"), 562)

    def test_part2(self):
        """Test part2"""
        pass
        # self.assertEqual(Day14.part2("../inputs/14/input_small_1.txt"), 286)
        # self.assertEqual(Day14.part2("../inputs/14/input.txt"), 101860)


if __name__ == "__main__":
    unittest.main()
