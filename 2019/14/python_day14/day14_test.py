#!/usr/bin/env python
from unittest import TestCase, main

from day14 import parse, part1, part2


class Day14TestCase(TestCase):
    def test_part1_small(self):
        rules = parse("../input_p1_31.txt")
        self.assertEqual(part1(rules), 31)
        rules = parse("../input_p1_165.txt")
        self.assertEqual(part1(rules), 165)
        rules = parse("../input_p1_13312.txt")
        self.assertEqual(part1(rules), 13312)

    def test_part1_large(self):
        rules = parse("../input_p1_180697.txt")
        self.assertEqual(part1(rules), 180697)
        rules = parse("../input_p1_2210736.txt")
        self.assertEqual(part1(rules), 2210736)

    def test_part1_input(self):
        rules = parse("../input.txt")
        self.assertEqual(part1(rules), 720484)

    def test_part2_examples(self):
        rules = parse("../input_p1_13312.txt")
        self.assertEqual(part2(rules), 82892753)
        rules = parse("../input_p1_180697.txt")
        self.assertEqual(part2(rules), 5586022)
        rules = parse("../input_p1_2210736.txt")
        self.assertEqual(part2(rules), 460664)

    def test_part2_input(self):
        rules = parse("../input.txt")
        self.assertEqual(part2(rules), 1993284)


if __name__ == "__main__":
    main()
