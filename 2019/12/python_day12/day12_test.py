#!/usr/bin/env python
from unittest import TestCase, main
from day12 import energy_after_steps, cycle_time, test_input, test_input2, real_input


class Day12TestCase(TestCase):
    def test_energy_after_steps(self):
        got = energy_after_steps(test_input(), 10)
        self.assertEqual(got, 179)

    def test_energy_after_steps2(self):
        got = energy_after_steps(test_input2(), 100)
        self.assertEqual(got, 1940)

    def test_cycle_time_1(self):
        got = cycle_time(test_input())
        self.assertEqual(got, 2772)

    def test_cycle_time_2(self):
        got = cycle_time(test_input2())
        self.assertEqual(got, 4686774924)

    def test_part1(self):
        got = energy_after_steps(real_input(), 1000)
        self.assertEqual(got, 10845)

    def test_part2(self):
        got = cycle_time(real_input())
        self.assertEqual(got, 551272644867044)


if __name__ == "__main__":
    main()
