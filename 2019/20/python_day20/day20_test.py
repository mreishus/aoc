#!/usr/bin/env python
from unittest import TestCase, main

from day20 import part1, part2


class Day20TestCase(TestCase):
    def test_part1_examples(self):
        got = part1("../../20/input_23.txt")
        want = 23
        self.assertEqual(got, want)

        got = part1("../../20/input_58.txt")
        want = 58
        self.assertEqual(got, want)

    def test_part1(self):
        got = part1("../../20/input.txt")
        want = 490
        self.assertEqual(got, want)

    def test_part2_examples(self):
        got = part2("../../20/input_recursive_396.txt")
        want = 396
        self.assertEqual(got, want)

    def test_part2(self):
        got = part2("../../20/input.txt")
        want = 5648
        self.assertEqual(got, want)


if __name__ == "__main__":
    main()
