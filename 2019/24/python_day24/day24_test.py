#!/usr/bin/env python
from unittest import TestCase, main

from day24 import Day24


class Day24TestCase(TestCase):
    def test_part1_examples(self):
        d24 = Day24("../../24/input_small.txt")
        got = d24.part1()
        want = 2129920
        self.assertEqual(got, want)

    def test_part1(self):
        d24 = Day24("../../24/input.txt")
        got = d24.part1()
        want = 25719471
        self.assertEqual(got, want)

    def test_part2_examples(self):
        d24 = Day24("../../24/input_small.txt")
        got = d24.part2(10)
        want = 99
        self.assertEqual(got, want)

    def test_part2(self):
        d24 = Day24("../../24/input.txt")
        got = d24.part2()
        want = 1916
        self.assertEqual(got, want)


if __name__ == "__main__":
    main()
