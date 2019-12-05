#!/usr/bin/env python
from unittest import TestCase, main
from day05 import add_one, decode


class Day05TestCase(TestCase):
    def test_fourdigit(self):
        want = (0, 1, 2, 34)
        got = decode(1234)
        self.assertEqual(want, got)

    def test_fivedigit(self):
        want = (1, 2, 3, 45)
        got = decode(12345)
        self.assertEqual(want, got)
        # (a, b, c, de) = decode(1234)
        # self.assertEqual(a, 1)
        # z = decode(99999)
        # print(z)

    def test_onedigit(self):
        want = (0, 0, 0, 1)
        got = decode(1)
        self.assertEqual(want, got)


if __name__ == "__main__":
    main()
