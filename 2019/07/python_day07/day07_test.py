#!/usr/bin/env python
from unittest import TestCase, main

from day07 import part1


class Day07TestCase(TestCase):
    def test_add_one(self):
        self.assertEqual(2, add_one(1))


if __name__ == "__main__":
    main()
