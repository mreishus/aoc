#!/usr/bin/env python
from unittest import TestCase, main
from day04 import is_password, is_password2, solve, solve2


class Day04TestCase(TestCase):
    def test_is_password(self):
        self.assertEqual(is_password(111111), True)
        self.assertEqual(is_password(223450), False)
        self.assertEqual(is_password(123789), False)
        self.assertEqual(is_password(123444), True)

    def test_is_password2(self):
        self.assertEqual(is_password2(111111), False)
        self.assertEqual(is_password2(223450), False)
        self.assertEqual(is_password2(123789), False)
        self.assertEqual(is_password2(112233), True)
        self.assertEqual(is_password2(123444), False)
        self.assertEqual(is_password2(111122), True)
        self.assertEqual(is_password2(111123), False)

    def test_solve(self):
        want = 771
        got = solve(200000, 300000)
        self.assertEqual(want, got)

    def test_solve2(self):
        want = 546
        got = solve2(200000, 300000)
        self.assertEqual(want, got)


if __name__ == "__main__":
    main()
