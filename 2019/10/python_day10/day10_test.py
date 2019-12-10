#!/usr/bin/env python
from unittest import TestCase, main

from day10 import part1, part2, parse


class Day10TestCase(TestCase):
    def test_part1_1(self):
        grid = parse("../input_small.txt")
        (x, y, count) = part1(grid)
        self.assertEqual(x, 3)
        self.assertEqual(y, 4)
        self.assertEqual(count, 8)

    def test_part1_2(self):
        grid = parse("../input_small2.txt")
        (x, y, count) = part1(grid)
        self.assertEqual(x, 5)
        self.assertEqual(y, 8)
        self.assertEqual(count, 33)

    def test_part1_3(self):
        grid = parse("../input_small3.txt")
        (x, y, count) = part1(grid)
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(count, 35)

    def test_part1_4(self):
        grid = parse("../input_small4.txt")
        (x, y, count) = part1(grid)
        self.assertEqual(x, 6)
        self.assertEqual(y, 3)
        self.assertEqual(count, 41)

    def test_part1_5(self):
        grid = parse("../input_small5.txt")
        (x, y, count) = part1(grid)
        self.assertEqual(x, 11)
        self.assertEqual(y, 13)
        self.assertEqual(count, 210)

    def test_part1_main(self):
        grid = parse("../input.txt")
        (x, y, count) = part1(grid)
        self.assertEqual(x, 11)
        self.assertEqual(y, 11)
        self.assertEqual(count, 221)

    def test_part2_1(self):
        grid = parse("../input_small5.txt")
        magic_num = part2(grid)
        self.assertEqual(magic_num, 802)

    def test_part2_main(self):
        grid = parse("../input.txt")
        magic_num = part2(grid)
        self.assertEqual(806, magic_num)


if __name__ == "__main__":
    main()
